use std::{net::{TcpListener, TcpStream}, io::{Write, Read}};
use std::cell::RefCell;

mod request;
mod tls;
mod server;

use mio::{Poll, Events};
use request::Request;

fn main() {
    let http = "127.0.0.1:7878".parse().unwrap();
    let https = "127.0.0.1:7879".parse().unwrap();

    let mut poll = Poll::new().expect("Couldn't create a mio::Poll");
    let mut events = Events::with_capacity(128);

    let mut token_generator = RefCell::new(server::TokenGenerator::new());

    let mut http_server = server::Server::new(http, &token_generator);
    let mut https_server = server::Server::new(https, &token_generator);

    poll.registry().register(&mut http_server.client, http_server.token, mio::Interest::READABLE).unwrap();
    poll.registry().register(&mut https_server.client, https_server.token, mio::Interest::READABLE).unwrap();

    loop {
        poll.poll(&mut events, None).unwrap();

        for event in events.iter() {
            match event.token() {
                token if token == http_server.token => {
                    http_server.accept();
                },
                token if token == https_server.token => {
                },
                _ => unreachable!(),
        }
    }

    // for stream in http_listener.incoming() {
    //     let stream = stream.unwrap();
    //     // stream.set_read_timeout(Some(std::time::Duration::new(5, 0))).expect("Couldn't set a read timeout");
    //     stream.set_nodelay(true).unwrap();
    //     let res = handle_request(stream);

    //     if res.is_err() {
    //         // do something
    //     }
    // }
}


fn handle_request(mut stream: TcpStream) -> Result<(), std::io::Error > {

    // let akingbee = "localhost".try_into().unwrap();
    let config = std::sync::Arc::new(tls::configure());
    let mut conn = rustls::ServerConnection::new(config).unwrap();

    let mut vec = Vec::new();

    loop {
        if conn.wants_read() {
            conn.read_tls(&mut stream).unwrap();
            conn.process_new_packets().unwrap();
            match conn.reader().read_to_end(&mut vec) {
                Ok(io) => {
                    break
                }
                Err(err) => {
                    if err.kind() == std::io::ErrorKind::WouldBlock {
                        println!("Would block")
                    } else {
                        println!("Would error")
                    }
                }
            }
            println!("{:?}", String::from_utf8_lossy(&vec));
        }

        else if conn.wants_write() {
            match conn.write_tls(&mut stream) {
                Ok(io) => println!("Wrote ! {}", io),
                Err(err) => {
                    if err.kind() == std::io::ErrorKind::WouldBlock {
                        println!("Blocking Error happened")
                    } else {
                        println!("Error happened")
                    };
                }
            };
            conn.process_new_packets().unwrap();
        }

    }



    let mut request = Request::build(&mut stream).unwrap();

    if request.uri.starts_with("/google/") {
        let mut stream = TcpStream::connect("google.com:443").unwrap();
        request.uri = request.uri.replacen("/google", "", 1);
        println!("request: {:?}", request.to_raw());
        stream.write(&request.to_raw().as_bytes()).unwrap();

        let mut buffer = [0; 1024];
        let bytes = stream.read(&mut buffer).unwrap();

        let res = String::from_utf8_lossy(&buffer[..bytes]);
        println!("answer: {:?}", res);
    }

    if request.uri.starts_with("/akingbee/") {
        let mut stream = TcpStream::connect("akingbee.com:80").unwrap();
        request.uri = request.uri.replacen("/akingbee", "", 1);
        println!("request: {}", request.to_raw());
        stream.write(&request.to_raw().as_bytes()).unwrap();

        let mut buffer = [0; 1024];
        let bytes = stream.read(&mut buffer).unwrap();

        let res = String::from_utf8_lossy(&buffer[..bytes]);
        println!("answer: {}", res);
    }

    let reply = format!("HTTP/1.1 200 OK\r\n\r\n");
    let reply = reply.as_bytes();
    stream.write(&reply).unwrap();

    Ok(())
}