import socket

#Server IP Address and Port to connect to
SERVER_IP = "127.0.0.1"
SERVER_PORT = 1082

# Implementing the TCP Socket to connect to server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((SERVER_IP, SERVER_PORT))
print("Connected to server", SERVER_IP, SERVER_PORT)

while True:
    # creating  user prompt to allow the user to enter a command
    user_input = input("> ")
    # Testing no entry from the user and having the prompt continue
    if user_input.strip() == "":
        continue
    # adding newline and convert to bytes, then send to server
    s.send((user_input + "\n").encode())
    # data reading up to 1024 bytes from the server
    data = s.recv(1024)
    if not data:
        break
    print(data.decode().strip())

# if user typed logout or shutdown, exit the client
    word = user_input.split()[0].upper()
    if word == "LOGOUT" or word == "SHUTDOWN":
        break

#close the socket and exit the client
s.close()
print("Client Left The Server")




