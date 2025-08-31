use hyper::{Body, Request, Response, Server};
use hyper::service::{make_service_fn, service_fn};
use rustls::ServerConfig;
use std::fs::File;
use std::io::BufReader;
use std::path::Path;

async fn handle_request(_req: Request<Body>) -> Result<Response<Body>, hyper::Error> {
    Ok(Response::new(Body::from("Hello, HTTPS World!")))
}

fn load_certs() -> Result<Vec<rustls::Certificate>, Box<dyn std::error::Error>> {
    let cert_path = Path::new("cert.pem");
    if !cert_path.exists() {
        return Err("Certificate file 'cert.pem' not found. Please generate certificates first.".into());
    }
    
    let cert_file = File::open(cert_path)?;
    let mut reader = BufReader::new(cert_file);
    let certs = rustls::internal::pemfile::certs(&mut reader)
        .map_err(|_| "Failed to parse certificate file")?;
    
    Ok(certs)
}

fn load_private_key() -> Result<rustls::PrivateKey, Box<dyn std::error::Error>> {
    let key_path = Path::new("key.pem");
    if !key_path.exists() {
        return Err("Private key file 'key.pem' not found. Please generate certificates first.".into());
    }
    
    let key_file = File::open(key_path)?;
    let mut reader = BufReader::new(key_file);
    
    // Try PKCS8 first, then PKCS1
    let keys = rustls::internal::pemfile::pkcs8_private_keys(&mut reader)
        .or_else(|_| {
            let key_file = File::open(key_path)?;
            let mut reader = BufReader::new(key_file);
            rustls::internal::pemfile::rsa_private_keys(&mut reader)
        })
        .map_err(|_| "Failed to parse private key file")?;
    
    if keys.is_empty() {
        return Err("No private keys found in key file".into());
    }
    
    Ok(keys[0].clone())
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("Loading certificates...");
    
    let certs = load_certs()?;
    let private_key = load_private_key()?;

    let mut config = ServerConfig::new(rustls::NoClientAuth::new());
    config.set_single_cert(certs, private_key)?;

    let addr = ([127, 0, 0, 1], 8443).into(); // Using 8443 instead of 443 to avoid privilege issues
    let make_svc = make_service_fn(|_conn| async { 
        Ok::<_, hyper::Error>(service_fn(handle_request)) 
    });

    println!("Starting HTTPS server on https://{}", addr);
    
    let server = Server::bind(&addr)
        .serve(make_svc);

    println!("Server started successfully!");
    println!("Test with: curl -k https://localhost:8443");
    
    if let Err(e) = server.await {
        eprintln!("Server error: {}", e);
        return Err(e.into());
    }

    Ok(())
}
