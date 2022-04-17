use std::convert::TryInto;
use std::sync::Arc;

use mio::{Token, Poll};
use mio::net::{TcpStream};
use mio::event::*;

use rustls::ServerConfig;

use crate::handler::{TlsHandler, HttpHandler, HandlerResponse};


pub struct Connection {
    pub stream: TcpStream,
    pub closing: bool,
    tls_conn: Option<rustls::ServerConnection>,
    to_write: String
}

impl Connection {

    pub fn new(stream: TcpStream, tls_config: &Option<Arc<ServerConfig>>) -> Connection {
        let conn: Option<rustls::ServerConnection> = match tls_config {
            Some(config) => Some(rustls::ServerConnection::new(config.clone()).unwrap()),
            None => None
        };
        Connection{stream: stream, closing: false, tls_conn: conn, to_write: String::new()}
    }

    fn read(&mut self) -> HandlerResponse {

        let data = match &mut self.tls_conn {
            Some(conn) => TlsHandler::read(&mut self.stream, conn),
            None => HttpHandler::read(&mut self.stream)
        };

        return data;
    }

    pub fn add_data_to_write(&mut self, data: String, poll: &Poll, token: Token) {
        self.to_write.push_str(&data);
        poll.registry().register(&mut self.stream, token, mio::Interest::WRITABLE).unwrap();
    }

    fn write(&mut self) {
        HttpHandler::write(&mut self.stream, self.to_write.as_bytes());
    }


    pub fn handle(&mut self, event: &Event) -> Result<HandlerResponse, std::io::Error> {
        if event.is_readable() {
            let response = self.read();
            if response.closing {
                self.closing = true;
            };

            if event.is_writable() {
                if self.tls_conn.is_some() {
                    let tls_response = TlsHandler::do_tls_write(&mut self.stream, self.tls_conn.as_mut().unwrap());
                    if tls_response.closing {
                        self.closing = true;
                    };
                }

                self.write();
            }


            return Ok(response);
        }

        return Ok(HandlerResponse::new());
    }

    pub fn to_close(&self) -> bool {
        self.closing
    }

    fn get_interest(&self) -> mio::Interest {
        if let Some(conn) = &self.tls_conn {
            let rd = conn.wants_read();
            let wr = conn.wants_write();

            if rd && wr {
                return mio::Interest::READABLE | mio::Interest::WRITABLE;
            } else if wr {
                return mio::Interest::WRITABLE;
            } else {
                return mio::Interest::READABLE;
            }
        } else {
            mio::Interest::READABLE.add(mio::Interest::WRITABLE)
        }
    }

    pub fn register(&mut self, poll: &mut Poll, token: Token) {
        let interest = self.get_interest();
        poll.registry().register(&mut self.stream, token, interest).unwrap();
    }

    pub fn reregister(&mut self, poll: &mut Poll, token: Token) {
        if self.tls_conn.is_none() {
            return;
        }

        let interest = self.get_interest();
        poll.registry().reregister(&mut self.stream, token, interest).unwrap();
    }

    pub fn deregister(&mut self, poll: &mut Poll) {
        poll.registry().deregister(&mut self.stream).unwrap()
    }

    pub fn shutdown(&mut self) -> bool {
        if self.tls_conn.is_some() {
            // last gasp
            TlsHandler::do_tls_write(&mut self.stream, self.tls_conn.as_mut().unwrap());
        }

        self.stream.shutdown(std::net::Shutdown::Both).is_ok()
    }
}