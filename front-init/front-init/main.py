from server_module import create_http_server, create_socket_server_thread

def main():
    # HTTP Server
    httpd = create_http_server()

    # Socket Server
    socket_server_thread = create_socket_server_thread()
    socket_server_thread.start()

    print("Servers are running.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    httpd.server_close()
    socket_server_thread.join()

if __name__ == '__main__':
    main()
