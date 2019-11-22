import socket

def main():
    host, port = "127.0.0.1", 6000
    sock = socket.socket()
    sock.connect((host, port))

    while True:
        message = sock.recv(1024).decode("utf-8")

        if message == "q":
            break
        else:
            response = input(message + "\n=> ")
            if response == "q":
                sock.send(response.encode("utf-8"))
                break
            else:
                sock.send(response.encode("utf-8"))
    sock.close()

if __name__ =="__main__":
    main()