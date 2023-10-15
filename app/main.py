from pathlib import PurePath
import socket


def main():
    # Create a TCP socket bound to local host
    with socket.create_server(("127.0.0.1", 4221), reuse_port=True) \
        as server_socket:
        
        while True:
            # Wait for the client connection
            client_socket, _ = server_socket.accept()

            # Get the data (as bytes) from the client socket
            client_data_buffer = client_socket.recv(4096)

            # Decode the bytes using UTF-8
            raw_http_request = client_data_buffer.decode(encoding="utf-8")
            
            # The HTTP message start line is the first line in the HTTP request
            http_msg_start_line = raw_http_request.split("\r\n")[0]

            # Get the path from the HTTP message start line
            path = http_msg_start_line.split(" ")[1]
            
            # Handle the request
            if path == "/":
                client_socket.send(b"HTTP/1.1 200 OK\r\n\r\n")
            elif path.startswith("/echo/"):
                resp = bytearray()
                resp.extend(b"HTTP/1.1 200 OK\r\n")
                resp.extend(b"Content-Type: text/plain\r\n")
                # Get the final path component
                body = f"{PurePath(path).name}\r\n\r\n".encode()
                resp.extend(f"Content-Length: {len(body)}\r\n\r\n".encode(encoding="utf-8"))
                resp.extend(body)
                client_socket.send(resp)
            else:
                client_socket.send(b"HTTP/1.1 404 Not Found\r\n\r\n")
            client_socket.close()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Goodbye!")
