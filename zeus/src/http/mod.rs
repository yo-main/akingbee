
use std::io::prelude::*;
use std::net::TcpStream;
use std::collections::HashMap;

#[derive(Debug)]
pub struct Request {
    pub method: String,
    pub uri: String,
    pub http_version: String,
    pub headers: HashMap<String, String>,
    pub body: String
}


pub fn build(stream: &mut TcpStream) -> Result<Request, std::io::Error> {
    let mut buffer = [0; 1024];
    let raw = std::cell::RefCell::new(String::new());
    let mut head: Vec<String> = Vec::new();
    let mut headers: HashMap<String, String> = HashMap::new();
    let mut body: String = String::new();

    loop {
        let bytes = stream.read(&mut buffer).expect("Couldn't read data from stream");

        raw.borrow_mut().push_str(&String::from_utf8_lossy(&buffer[..bytes]));


        let body_start = raw.borrow().find("\r\n\r\n");

        if body_start.is_none() {
            continue; // headers not yet all received
        };
        println!("{:?}", raw);

        if head.is_empty() {
            let metadata: Vec<String> = raw.borrow()[..body_start.unwrap()].split("\r\n").map(|t| String::from(t)).collect();
            head = metadata[0].split(" ").map(|t| String::from(t.trim())).collect();

            if head.len() != 3 {
                panic!("Incorrect head (expected method, uri & http version)");
            }

            for row in &metadata[1..] {
                let item: Vec<&str> = row.split(":").collect();
                headers.insert(String::from(item[0].trim()), String::from(item[1].trim()));
            }
        }

        if headers.contains_key("Content-Type") {
            let content_length: usize = headers.get("Content-Length").unwrap().parse().unwrap();
            if (raw.borrow().chars().count() - body_start.unwrap()) < content_length {
                continue;
            }
        }

        body.push_str(&raw.borrow()[body_start.unwrap()..].trim());

        break;
    }

    return Ok(Request{
        http_version: head.pop().unwrap(), // 2
        uri: head.pop().unwrap(), // 1
        method: head.pop().unwrap(), // 0
        headers: headers,
        body: body
    });
}
