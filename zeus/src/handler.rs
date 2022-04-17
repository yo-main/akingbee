use std::io::{Read, Write};

use mio::net::TcpStream;

pub struct HttpHandler;
pub struct TlsHandler;

pub struct HandlerResponse {
    pub data: String,
    pub closing: bool,
    pub error: bool
}

impl HandlerResponse {
    fn from_err(err: std::io::Error, closing: bool) -> HandlerResponse {
        HandlerResponse{data: err.to_string(), closing: closing, error: true}
    }

    fn from_string(data: String, close: bool) -> HandlerResponse {
        HandlerResponse{data: data, closing: close, error: false}
    }

    pub fn new() -> HandlerResponse {
        HandlerResponse{data: String::new(), closing: false, error: false}
    }
}

impl HttpHandler {
    pub fn write(stream: &mut TcpStream, data: &[u8]) {
        stream.write(data).unwrap();
    }

    pub fn read(stream: &mut TcpStream) -> HandlerResponse {
        let mut received_data = vec![0; 4096];
        let mut bytes_read = 0;
        let mut closing = false;
        // We can (maybe) read from the connection.
        loop {
            match stream.read(&mut received_data[bytes_read..]) {
                Ok(0) => {
                    // Reading 0 bytes means the other side has closed the
                    // connection or is done writing, then so are we.
                    closing = true;
                    break;
                }
                Ok(n) => {
                    bytes_read += n;
                    if bytes_read == received_data.len() {
                        received_data.resize(received_data.len() + 1024, 0);
                    }
                }
                // Would block "errors" are the OS's way of saying that the
                // connection is not actually ready to perform this I/O operation.
                Err(ref err) if err.kind() == std::io::ErrorKind::WouldBlock => break,
                Err(ref err) if err.kind() == std::io::ErrorKind::Interrupted => continue,
                // Other errors we'll consider fatal.
                Err(err) => return HandlerResponse::from_err(err, true),
            }
        }

        return HandlerResponse::from_string(String::from_utf8_lossy(&received_data[..bytes_read]).to_string(), closing);
    }
}


impl TlsHandler {

    pub fn read(stream: &mut TcpStream, tls_conn: &mut rustls::ServerConnection) -> HandlerResponse {
        let data = if tls_conn.wants_read() {
            match tls_conn.read_tls(stream) {
                Ok(0) => HandlerResponse::from_string(String::new(), true),
                Ok(_) => TlsHandler::try_plain_read(tls_conn),
                Err(err) if err.kind() == std::io::ErrorKind::WouldBlock => HandlerResponse::from_err(err, false),
                Err(err) if err.kind() == std::io::ErrorKind::Interrupted => TlsHandler::read(stream, tls_conn),
                Err(err) => HandlerResponse::from_err(err, true),
            }
        } else { HandlerResponse::new() };

        if tls_conn.wants_write() {
            let response = TlsHandler::do_tls_write(stream, tls_conn);
            if response.error {return response}
        }

        return data;
    }

    pub fn do_tls_write(stream: &mut TcpStream, tls_conn: &mut rustls::ServerConnection) -> HandlerResponse {
        match tls_conn.write_tls(stream) {
            Ok(_) => HandlerResponse::new(),
            Err(err) => {
                HandlerResponse::from_err(err, true)
            }
        }
    }

    fn try_plain_read(tls_conn: &mut rustls::ServerConnection) -> HandlerResponse {
        let mut vec = Vec::new();
        if let Ok(io_state) = tls_conn.process_new_packets() {
            if io_state.plaintext_bytes_to_read() > 0 {
                vec.resize(io_state.plaintext_bytes_to_read(), 0u8);

                tls_conn.reader().read_exact(&mut vec).unwrap();
            }
        }
        return HandlerResponse::from_string(String::from_utf8_lossy(&vec).to_string(), false);
    }

}