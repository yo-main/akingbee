use std::{net::{TcpListener, TcpStream}, io::Write};


mod http;

fn main() {
    let listener = TcpListener::bind("127.0.0.1:7878").unwrap();
    for stream in listener.incoming() {
        let stream = stream.unwrap();
        // stream.set_read_timeout(Some(std::time::Duration::new(5, 0))).expect("Couldn't set a read timeout");
        stream.set_nodelay(true).unwrap();
        let res = handle_request(stream);

        if res.is_err() {
            // do something
        }
    }
}


fn handle_request(mut stream: TcpStream) -> Result<(), std::io::Error > {

    let request = http::build(&mut stream).unwrap();

    println!("{:?}", request);

    let reply = format!("HTTP/1.1 200 OK\r\n\r\nrequest: {}\n", request.body);
    let reply = reply.as_bytes();
    stream.write(&reply).unwrap();

    Ok(())
}