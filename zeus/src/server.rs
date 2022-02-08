use std::collections::HashMap;

use std::cell::RefCell;

use mio::{Token};
use mio::net::{TcpListener, TcpStream};

use rustls::ServerConfig;

const SERVER: Token = Token(0);


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


struct Connection {
    stream: TcpStream
}

pub struct Server <'a> {
    pub client: TcpListener,
    pub token: Token,
    connections: HashMap<Token, Connection>,
    token_generator: &'a RefCell<TokenGenerator>,
}

impl <'a> Server <'a> {
    pub fn new(address: std::net::SocketAddr, token_generator: &'a RefCell<TokenGenerator>) -> Server {
        Server {
            client: TcpListener::bind(address).unwrap(),
            token: token_generator.borrow_mut().incr(),
            connections: HashMap::new(),
            token_generator: token_generator,
        }
    }
}

// fn main() {
//     let http_listener = TcpListener::bind("127.0.0.1:7878").unwrap();
//     for stream in http_listener.incoming() {
//         let stream = stream.unwrap();
//         // stream.set_read_timeout(Some(std::time::Duration::new(5, 0))).expect("Couldn't set a read timeout");
//         stream.set_nodelay(true).unwrap();
//         let res = handle_request(stream);

//         if res.is_err() {
//             // do something
//         }
//     }
// }


// fn handle_request(mut stream: TcpStream) -> Result<(), std::io::Error > {

//     // let akingbee = "localhost".try_into().unwrap();
//     let config = std::sync::Arc::new(tls::configure());
//     let mut conn = rustls::ServerConnection::new(config).unwrap();

//     let mut vec = Vec::new();

//     loop {
//         if conn.wants_read() {
//             conn.read_tls(&mut stream).unwrap();
//             conn.process_new_packets().unwrap();
//             match conn.reader().read_to_end(&mut vec) {
//                 Ok(io) => {
//                     break
//                 }
//                 Err(err) => {
//                     if err.kind() == std::io::ErrorKind::WouldBlock {
//                         println!("Would block")
//                     } else {
//                         println!("Would error")
//                     }
//                 }
//             }
//             println!("{:?}", String::from_utf8_lossy(&vec));
//         }

//         else if conn.wants_write() {
//             match conn.write_tls(&mut stream) {
//                 Ok(io) => println!("Wrote ! {}", io),
//                 Err(err) => {
//                     if err.kind() == std::io::ErrorKind::WouldBlock {
//                         println!("Blocking Error happened")
//                     } else {
//                         println!("Error happened")
//                     };
//                 }
//             };
//             conn.process_new_packets().unwrap();
//         }

//     }



//     let mut request = Request::build(&mut stream).unwrap();

//     if request.uri.starts_with("/google/") {
//         let mut stream = TcpStream::connect("google.com:443").unwrap();
//         request.uri = request.uri.replacen("/google", "", 1);
//         println!("request: {:?}", request.to_raw());
//         stream.write(&request.to_raw().as_bytes()).unwrap();

//         let mut buffer = [0; 1024];
//         let bytes = stream.read(&mut buffer).unwrap();

//         let res = String::from_utf8_lossy(&buffer[..bytes]);
//         println!("answer: {:?}", res);
//     }

//     if request.uri.starts_with("/akingbee/") {
//         let mut stream = TcpStream::connect("akingbee.com:80").unwrap();
//         request.uri = request.uri.replacen("/akingbee", "", 1);
//         println!("request: {}", request.to_raw());
//         stream.write(&request.to_raw().as_bytes()).unwrap();

//         let mut buffer = [0; 1024];
//         let bytes = stream.read(&mut buffer).unwrap();

//         let res = String::from_utf8_lossy(&buffer[..bytes]);
//         println!("answer: {}", res);
//     }

//     let reply = format!("HTTP/1.1 200 OK\r\n\r\n");
//     let reply = reply.as_bytes();
//     stream.write(&reply).unwrap();

//     Ok(())
// }