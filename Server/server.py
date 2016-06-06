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


# def get_page(path):

    #http://www.blog.pythonlibrary.org/2013/10/29/python-101-how-to-find-the-path-of-a-running-script/


def get_file(path):
    file_io = open(path.replace("//", "/"), 'rb')
    file = file_io.read()
    return file


class BaseServer:

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_name = ""
    server_path = ""
    server_www_path = ""

    host_name = "0.0.0.0"

    host_port = 8001  # default port
    is_shutdown = False

    def __init__(self, name):
        self.server_name = name
        self.server_path = os.path.dirname(sys.argv[0])
        self.server_www_path = self.server_path + "/www"
        
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
        media = [False, ""]
        code, file_path = self.parse_request(connection.recv(buffer_size))
        full_path = self.server_www_path + "/" + file_path
        if str(file_path).endswith(tuple([".png", ".jpg", ".gif"])):
            if str(file_path).endswith(".gif"):
                media[1] = "gif"
            else:
                media[1] = "jpeg"

            page = get_file(full_path)
            media[0] = True
        else:
            page = get_file(full_path).decode("utf-8")

        response_headers, data = self.parse_response(code, page, media)
        if type(data) == bytes:
            connection.send(bytes(response_headers.encode("utf-8")))
            connection.sendall(data)
        else:
            connection.send(bytes((response_headers + data).encode("utf-8")))


    def parse_request(self, data):
        if len(data) == 0:
            return
        strings = str(bytes(data).decode('utf-8')).split('\r\n')
        command, path, version = strings[0].split()
        print("command - " + command)
        print("path - " + path)
        print("version - " + version)

        # status = 1
        file = "/not-found.html"
        code = 200
        if path == "/":
            file = "/index.html"
        elif self.is_file_exist(path):
            file = path
        else:
            code = 404

        return code, file


    def parse_response(self, code, page, media):
        status = "ERROR"

        if code == 200:
            status = "OK"
        elif code == 404:
            status = "NOT FOUND"
        base_header = (default_header_status % {'code': code, 'status': status})
        if not media[0]:
            base_content_type = default_header_content_type
        else:
            base_content_type = "Content-Type: image/"+media[1]+"\r\n\r\n"

        # return_string = str(base_header + base_content_type + page)

        return base_header + base_content_type, page

    def is_file_exist(self, path):
        full_path = self.server_www_path + path
        return os.path.isfile(full_path)

    def check_if_shutdown(self):
        pass


def main():
    server = BaseServer("Home Server")
    server.start_server()
    

if __name__ == "__main__":
    main()
