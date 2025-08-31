@echo off
echo Testing all Rust network protocol projects...

echo Testing HTTPS Server...
cd https-server
cargo build
if %errorlevel% equ 0 (
    echo ✓ HTTPS Server compiles successfully
) else (
    echo ✗ HTTPS Server compilation failed
)
cd ..

echo Testing FTP Server...
cd ftp-server
cargo build
if %errorlevel% equ 0 (
    echo ✓ FTP Server compiles successfully
) else (
    echo ✗ FTP Server compilation failed
)
cd ..

echo Testing SSH Server...
cd ssh-server
cargo build
if %errorlevel% equ 0 (
    echo ✓ SSH Server compiles successfully
) else (
    echo ✗ SSH Server compilation failed
)
cd ..

echo Testing SMTP Server...
cd smtp-server
cargo build
if %errorlevel% equ 0 (
    echo ✓ SMTP Server compiles successfully
) else (
    echo ✗ SMTP Server compilation failed
)
cd ..

echo Testing DNS Server...
cd dns-server
cargo build
if %errorlevel% equ 0 (
    echo ✓ DNS Server compiles successfully
) else (
    echo ✗ DNS Server compilation failed
)
cd ..

echo Testing Raw Sockets...
cd raw-sockets
cargo build
if %errorlevel% equ 0 (
    echo ✓ Raw Sockets compiles successfully
) else (
    echo ✗ Raw Sockets compilation failed
)
cd ..

echo All projects tested!
pause
