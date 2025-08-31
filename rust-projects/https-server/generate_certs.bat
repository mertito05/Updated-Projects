@echo off
echo Generating self-signed certificates for HTTPS server...

REM Generate private key
openssl genrsa -out key.pem 2048

REM Generate certificate signing request
openssl req -new -key key.pem -out csr.pem -subj "/CN=localhost"

REM Generate self-signed certificate
openssl x509 -req -days 365 -in csr.pem -signkey key.pem -out cert.pem

REM Clean up CSR
del csr.pem

echo Certificates generated successfully:
echo - cert.pem (certificate)
echo - key.pem (private key)
echo.
echo Place these files in the project root directory before running the server.
