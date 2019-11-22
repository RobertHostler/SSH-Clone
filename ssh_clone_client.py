import socket
import crypt
import os


def client_input(client, prompt):
    client.send(prompt.encode("utf-8"))
    client_response = client.recv(1024).decode("utf-8")
    return client_response

def login(client, socket):
    password_tries = 3
    while password_tries > 0:
        username = client_input(client, "Please enter your username:")
        password = client_input(client, "Please enter your password:")

        if username_exists(username) and password_matches(username, password):
            return True
        else:
            client.send("Your username or password is incorrect. Try again.\n".encode("utf-8"))
            password_tries -= 1

    client.send("q".encode("utf-8"))
    client.close()
    socket.close()
    quit()

def username_exists(username):
    with open("credentials.txt", "r") as credentials:
        for line in credentials.readlines():
            components = line.split(":")
            savedusername = components[0].strip()

            if username == savedusername:
                return True
        else:
            return False

def password_matches(username, password):
    password_hash = crypt.crypt(password, salt='METHOD_BLOWFISH')
    with open("credentials.txt", "r") as credentials:
        for line in credentials.readlines():
            components = line.split(":")
            savedusername = components[0].strip()
            savedhash = components[1].strip()

            if username == savedusername:
                if password_hash == savedhash:
                    return True
        else:
            return False

def main():
    host, port = "127.0.0.1", 5000
    sock = socket.socket()
    sock.bind((host, port))
    sock.listen(1)
    client, addr = sock.accept()
    print("Connection from: " + str(addr))

    if not login(client, "Please log in to the SSH server:"):
        quit()

    while True:
        bash_command = client_input(client, "user@SSHclone:" + os.getcwd())
        if bash_command == "q":
            break
        else:
            os.system(bash_command)

    client.close()
    sock.close()


if __name__ == "__main__":
    main()