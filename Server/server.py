import socket
import threading
import os

hostName = ""
hostPort = 8080

listen = True
connected = False

times_connected = 0


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def cls():
    os.system("cls")
    print("server is listening...")


def start_server():
    """Start the server"""
    print("starting the server...")
    server_socket.bind((hostName, hostPort))
    while listen:
        print("server is listening...")
        server_socket.listen()
        conn, addr = server_socket.accept()
        global times_connected
        with conn:
            # if not connected:
            #     global connected
            #     connected = False
            print(addr, "\n------------------------ Connected!----------------------------------")
            byts = conn.recv(1024)
            if len(byts) == 0:
                print('-------------------no data --------------------------------')
                continue
            recv_data = str(byts)
            # if(recv_data.find("GET"))
            print(recv_data)
            conn.send(bytes("HTTP/1.1 200 OK\nContent-Type: text/html\n\n"
                            "<html>Hello World<br>newLine</html>"
                            .encode("utf-8")))
            s = 'times connected - ' + str(times_connected)

            conn.send(bytes(s.encode()))
            # conn.sendfile("/index.html")
            conn.close()
        times_connected += 1


def close_server():
    """Close the server"""
    try:
        print("1")
        # if connected:
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((hostName, hostPort))
        print("2")
        server_socket.close()
        print("3")
        pass
    except socket.error:
        pass

t = threading.Thread(None, start_server, "server")
t.start()
while True:
    inp = input("command:  \n")
    if inp == "exit":
        listen = False
        close_server()

        print("4")
        try:
            t.join(1)
        except RuntimeError as thr_err:
            print(thr_err)
        print("5")
        break
    if inp == "cls":
        cls()
print("should exit")

