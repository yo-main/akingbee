use std::cell::RefCell;
use std::net::{TcpStream, SocketAddr, ToSocketAddrs};

mod request;
mod tls;
mod server;
mod handler;
mod connection;

use mio::{Poll, Events};

fn main() {
    let http = "127.0.0.1:7878".parse().unwrap();
    let https = "127.0.0.1:7879".parse().unwrap();

    let mut poll = Poll::new().expect("Couldn't create a mio::Poll");
    let mut events = Events::with_capacity(128);

    let token_generator = RefCell::new(server::TokenGenerator::new());

    let mut servers: Vec<server::Server> = vec![
        server::Server::new(http, &token_generator, None),
        server::Server::new(https, &token_generator, Some(tls::configure())),
    ];

    servers.iter_mut().for_each(
        |server| poll.registry().register(&mut server.client, server.server_token, mio::Interest::READABLE).unwrap()
    );

    loop {
        poll.poll(&mut events, None).unwrap();

        for event in events.iter() {
            let token = event.token();
            println!("Processing event: {event:?}");
            if !servers.iter_mut().any(|server| server.process_event(&event, &token, &mut poll)) {
                panic!("Couldn't process the event")
            }
        }
    }
}