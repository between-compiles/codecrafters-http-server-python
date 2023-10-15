import socket


def main():
    # Create a TCP socket bound to local host
    with socket.create_server(("127.0.0.1", 4221), reuse_port=True) as server_socket:
        client_socket, _ = server_socket.accept() # wait for client
        client_data = client_socket.recv(4096)
        http_request = client_data.decode()
        http_msg_start_line = http_request.split("\r\n")[0]
        _, path, _ = http_msg_start_line.split(" ")
        if path == "/":
            client_socket.send(b"HTTP/1.1 200 OK\r\n\r\n")
        else:
            client_socket.send(b"HTTP/1.1 404 Not Found\r\n\r\n")
        client_socket.close()


if __name__ == "__main__":
    main()
