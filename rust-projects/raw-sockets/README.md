# Raw Socket Examples

Examples of TCP and UDP socket programming in Rust using Tokio for asynchronous networking.

## Features

- TCP server and client examples
- UDP server and client examples
- Asynchronous I/O with Tokio
- Echo server functionality for both protocols
- Interactive menu for selecting which example to run

## Usage

### Running the Examples

```bash
cd rust-projects/raw-sockets
cargo run
```

You will be presented with a menu to choose which example to run:

1. **TCP Server** - Listens on port 8080 and echoes back received messages
2. **TCP Client** - Connects to TCP server on 127.0.0.1:8080 and sends a test message
3. **UDP Server** - Listens on port 8081 and echoes back received datagrams
4. **UDP Client** - Sends a datagram to UDP server on 127.0.0.1:8081 and waits for response

### Testing the Examples

1. First run the TCP server (option 1)
2. In another terminal, run the TCP client (option 2)
3. You should see the message being sent and echoed back

Similarly for UDP:
1. First run the UDP server (option 3)
2. In another terminal, run the UDP client (option 4)
3. You should see the datagram being sent and echoed back

## Code Structure

- `tcp_server()` - Asynchronous TCP echo server
- `tcp_client()` - TCP client that sends a test message
- `udp_server()` - Asynchronous UDP echo server
- `udp_client()` - UDP client that sends a test datagram

## Future Enhancements

- Add support for multiple concurrent connections
- Implement more complex protocol examples
- Add configuration options via command line arguments
- Support for different message formats and protocols
- Performance benchmarking
