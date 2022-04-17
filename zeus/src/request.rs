
use std::io::prelude::*;
use std::net::TcpStream;
use std::collections::HashMap;

#[derive(Debug)]
pub struct Request <'a> {
    pub method: &'a str,
    pub uri: &'a str,
    pub http_version: &'a str,
    pub headers: HashMap<&'a str, &'a str>,
    pub body: &'a str,
}

impl <'a> Request <'a> {

    pub  fn build(data: &'a String) -> Result<Request, std::io::Error> {
        let header_start = data.find("\r\n").expect("Incorrect HTTP message");
        let body_start = data.find("\r\n\r\n").expect("Incorrect HTTP message");

        let metadata: Vec<&str> = data[..header_start].splitn(3, " ").collect();

        // let headers: HashMap<&str, &str> = data[header_start+2..body_start].split("\r\n").collect::<Vec<&str>>().iter().map(|r| r.split_once(":")).map(|r| return r.expect("Incorrect header")).map(|items| (items.0, items.1)).collect();
        let headers: HashMap<&str, &str> = data[header_start+2..body_start].split("\r\n").map(|r| r.split_once(":").map(|items| (items.0.trim(), items.1.trim())).expect("Incorrect headers")).collect();
        let body: &str = &data[body_start..].trim();

        return Ok(Request{
            method: metadata.get(0).unwrap().trim(),
            uri: metadata.get(1).unwrap().trim(),
            http_version: metadata.get(2).unwrap().trim(),
            headers: headers,
            body: body,
        });
    }

    pub fn to_raw(&self) -> String {
        let head = format!("{} {} {}", self.method, self.uri, self.http_version);
        let headers: String = self.headers.iter().map(|(k, v)| format!("{}: {}", k, v)).collect::<Vec<String>>().join("\r\n");
        let body: &str = &self.body;

        return head + "\r\n" + headers.as_str() + "\r\n\r\n" + body;
    }
}
