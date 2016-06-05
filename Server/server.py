import socket
import threading
import os
import sys

default_error_page = """\
<!DOCTYPE HTML>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html;charset=utf-8">
        <title>Error response</title>
    </head>

    <body>
    <center>
        <h1>Response</h1>
        <p>Error code: %(code)d</p>
        <p>Message: %(status)s.</p>
    </center>
    </body>
</html>
"""

default_header_status = "HTTP/1.1 %(code)d %(status)s\r\n"
default_header_content_type = "Content-Type: text/html; charset=utf-8\r\n\r\n"
buffer_size = 1024


def get_page(code,status):
    page = default_error_page % {'code': code, 'status': status}
    if code == 200:
        pass
    else:
        #http://www.blog.pythonlibrary.org/2013/10/29/python-101-how-to-find-the-path-of-a-running-script/
        cwd = os.path.abspath(os.path.dirname(sys.argv[0]))
        file = open(cwd + "/www/not-found.html", 'r')
        page = file.read()
    return page

class BaseServer:

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_name = ""
    host_name = "0.0.0.0"
    host_port = 8000  # default port
    is_shutdown = False

    def __init__(self, name):
        self.server_name = name

        
    def start_server(self):
        print('server starting...')
        thread = threading.Thread(target=self.run_server, name=self.server_name)
        print('starting main server thread...')
        thread.start()



    def run_server(self):
        print('Serving HTTP on %s port %s ...' % (self.host_name, self.host_port))
        self.server_socket.bind((self.host_name, self.host_port))  # bind to host
        self.server_socket.listen(5)
        while not self.is_shutdown:
            conn, addr = self.server_socket.accept()
            self.handle_request(conn, addr)

    def stop_server(self):
        pass

    def handle_request(self, connection, address):
        print('Connected from %s:%d' % (address[0], address[1]))
        result = self.parse_request(connection.recv(buffer_size))
        if result == 0:
            page = self.parse_response(200)
        else:
            page = self.parse_response(404)
        connection.sendall(bytes(page))

    def parse_request(self, data):
        if len(data) == 0:
            return
        strings = str(bytes(data).decode('utf-8')).split('\r\n')
        command, path, version = strings[0].split()
        print("command - " + command)
        print("path - " + path)
        print("version - " + version)

        status = 1

        if path == "/":
            status = 0

        return status

    def parse_response(self, code):
        status = "ERROR"
        if code == 200:
            status = "OK"
        elif code == 404:
            status = "NOT FOUND"

        base_header = (default_header_status % {'code': code, 'status': status})
        base_content_type = default_header_content_type
        # page = (default_error_page % {'code': code, 'status': status})
        page = str(get_page(code, status))
        return_string = str(base_header + base_content_type + page).encode('utf-8')
        return return_string

    def check_if_shutdown(self):
        pass


def main():
    server = BaseServer("Home Server")
    server.start_server()
    


    
if __name__ == "__main__":
    main()
