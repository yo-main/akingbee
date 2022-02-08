use rustls::{RootCertStore, OwnedTrustAnchor, ServerConfig};



fn get_root_store() -> RootCertStore {
    let mut root_store = RootCertStore::empty();
    root_store.add_server_trust_anchors(
        webpki_roots::TLS_SERVER_ROOTS
            .0
            .iter()
            .map(|ta| {
                OwnedTrustAnchor::from_subject_spki_name_constraints(
                    ta.subject,
                    ta.spki,
                    ta.name_constraints,
                )
            }
        )
    );

    return root_store;
}

fn load_certs(filename: &str) -> Vec<rustls::Certificate> {
    let certfile = std::fs::File::open(filename).expect("cannot open certificate file");
    let mut reader = std::io::BufReader::new(certfile);
    rustls_pemfile::certs(&mut reader)
        .unwrap()
        .iter()
        .map(|v| rustls::Certificate(v.clone()))
        .collect()
}

fn load_private_key(filename: &str) -> rustls::PrivateKey {
    let keyfile = std::fs::File::open(filename).expect("cannot open private key file");
    let mut reader = std::io::BufReader::new(keyfile);

    loop {
        match rustls_pemfile::read_one(&mut reader).expect("cannot parse private key .pem file") {
            Some(rustls_pemfile::Item::RSAKey(key)) => return rustls::PrivateKey(key),
            Some(rustls_pemfile::Item::PKCS8Key(key)) => return rustls::PrivateKey(key),
            None => break,
            _ => {}
        }
    }

    panic!(
        "no keys found in {:?} (encrypted keys not supported)",
        filename
    );
}


pub fn configure() -> ServerConfig {
    let certs = load_certs("keys/dev.cert.pem");
    let privkey = load_private_key("keys/dev.priv.pem");

    let config = ServerConfig::builder()
    .with_safe_default_cipher_suites()
    .with_safe_default_kx_groups()
    .with_protocol_versions(&rustls::ALL_VERSIONS.to_vec())
    .expect("Ok")
    .with_client_cert_verifier(rustls::server::NoClientAuth::new())
    .with_single_cert_with_ocsp_and_sct(certs, privkey, vec![], vec![]);

    return config.unwrap();
}