use std::collections::HashMap;

use std::cell::RefCell;
use std::hash::Hash;
use std::net::{SocketAddr, ToSocketAddrs};
use std::sync::Arc;

use mio::{Token, Poll};
use mio::net::{TcpStream, TcpListener};
use mio::event::*;

use crate::connection::Connection;
use crate::request::Request;

pub struct TokenGenerator {
    id: usize
}

impl TokenGenerator {
    pub fn new() -> TokenGenerator {
        TokenGenerator{id: 0}
    }

    fn incr(&mut self) -> Token {
        let token = Token(self.id);
        self.id += 1;
        return token;
    }
}

struct Forwarder <'a> {
    connections: HashMap<Token, [&'a Connection; 2]>
}

pub struct Server <'a> {
    pub client: TcpListener,
    pub server_token: Token,
    token_generator: &'a RefCell<TokenGenerator>,
    connections: HashMap<Token, Connection>,
    forwards: HashMap<Token, Token>,
    tls_config: Option<Arc<rustls::ServerConfig>>
}


impl <'a> Server <'a> {
    pub fn new(address: std::net::SocketAddr, token_generator: &'a RefCell<TokenGenerator>, tls_config: Option<rustls::ServerConfig>) -> Server {
        let mut generator = token_generator.borrow_mut();
        let config = match tls_config {
            Some(config) => Some(Arc::new(config)),
            None => None
        };

        Server {
            client: TcpListener::bind(address).unwrap(),
            token_generator: token_generator,
            server_token: generator.incr(),
            connections: HashMap::new(),
            forwards: HashMap::new(),
            tls_config: config,
        }
    }

    fn accept_incoming_connection(&mut self, poll: &mut Poll) -> Result<(), std::io::Error> {
        loop {
            let (stream, _address) = match self.client.accept() {
                Ok((stream, address)) => (stream, address),
                Err(e) if e.kind() == std::io::ErrorKind::WouldBlock => {
                    // If we get a `WouldBlock` error we know our listener has no more incoming connections queued
                    // so we can return to polling and wait for some more.
                    break;
                }
                Err(e) => {
                    return Err(e);
                }
            };

            let token = self.token_generator.borrow_mut().incr();

            let mut connection = Connection::new(stream, &self.tls_config);
            connection.register(poll, token);
            self.connections.insert(token, connection);
        }

        return Ok(());
    }

    pub fn process_event(&mut self, event: &Event, token: &Token, poll: &mut Poll) -> bool {
        if *token == self.server_token {
            return self.accept_incoming_connection(poll).is_ok();
        }

        let mut connection = self.connections.get_mut(token);
        let mut request: Option<Request> = None;

        if connection.is_some() {
            let connection = connection.as_mut().unwrap();
            match connection.handle(event) {
                Ok(response) => {

                    if !response.error && !response.data.is_empty() {
                        request = Some(Request::build(&response.data).unwrap());

                    };

                    if connection.to_close() {
                        println!("Closing connection");
                        connection.deregister(poll);
                        connection.shutdown();
                        self.connections.remove(token);
                    } else {
                        connection.reregister(poll, *token);
                    }
                    return true;
                },
                Err(_) => return false
            }
        };

        if request.is_some() {
            let mut request = request.unwrap();
            if request.uri.contains("/google/") {
                let google = "google.com:80".to_socket_addrs().unwrap().nth(0).unwrap();
                let stream = TcpStream::connect(google).unwrap();
                let mut conn = Connection::new(stream, &None);
                request.uri = "https://google.com/search";
                let raw = request.to_raw();

                let token = self.token_generator.borrow_mut().incr();
                conn.add_data_to_write(raw, poll, token);
                self.connections.insert(token, conn);
            }
        }

        return false;
    }
}