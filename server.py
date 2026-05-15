import socket
import os
import math

SERVER_PORT = 1082
# creating a list for the users
users_login = {}

f = open("logins.txt", "r")
for line in f:
    parts = line.split()
    if len(parts) == 2:
        users_login[parts[0]] = parts[1]
f.close()
print("User Log In:", list(users_login.keys()))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', SERVER_PORT))
s.listen(1)
print("Loading Port", SERVER_PORT)

shut_down = False
while not shut_down:
    print("waiting for connection")
    connect, addr = s.accept()
    print("Client has been connected from", addr)

    logged_in = False
    current_user_logged_in = None

    while True:
        data_input = connect.recv(1024)
        if not data_input:
            break

        message = data_input.decode()
        print("Data has been sent", message)

        arguments = message.split()
        if len(arguments) == 0:
            command_response = "301 message format error"
            connect.send((command_response + "\n").encode())
            continue

        commands = arguments[0].upper()
        args = arguments[1:]

        # Creating LOGIN command
        if commands == "LOGIN":
            if len(args) != 2:
                command_response = "301 message format error"
            elif args[0] in users_login and users_login[args[0]] == args[1]:
                logged_in = True
                current_user_logged_in = args[0]   # FIX: was args[1] (the password)
                command_response = "SUCCESS"
            else:
                command_response = "FAILURE: Please provide correct username and password, Please try again."

        # Creating the SOLVE command
        elif commands == "SOLVE":
            if not logged_in:
                command_response = "User not logged in, Please log in first."
            elif len(args) == 0:
                command_response = "300 invalid command"

            # Solving for Circle
            elif args[0] == "-c":
                if len(args) < 2:
                    command_response = "Cannot Find The Radius Of The Circle"
                    solution_file = open(current_user_logged_in + "_solutions.txt", "a")
                    solution_file.write("   " + command_response + "\n")
                    solution_file.close()
                else:
                    try:
                        radius = float(args[1])
                        circumference = 2 * math.pi * radius
                        area = math.pi * radius * radius
                        command_response = "Circle's circumference is %.2f and area is %.2f" % (circumference, area)
                        logged_in_data = "   radius %s: %s" % (args[1], command_response)
                        solution_file = open(current_user_logged_in + "_solutions.txt", "a")
                        solution_file.write(logged_in_data + "\n")
                        solution_file.close()
                    except ValueError:
                        command_response = "Radius must be a integer NOT a string"

            # Solving for Rectangle
            elif args[0] == "-r":
                if len(args) < 2:
                    command_response = "Cannot find the sides of the rectangle"
                    solution_file = open(current_user_logged_in + "_solutions.txt", "a")
                    solution_file.write("   " + command_response + "\n")
                    solution_file.close()
                else:
                    try:
                        rectangle_side1 = float(args[1])
                        if len(args) >= 3:
                            rectangle_side2 = float(args[2])
                        else:
                            rectangle_side2 = rectangle_side1

                        perimeter = 2 * (rectangle_side1 + rectangle_side2)
                        area = rectangle_side1 * rectangle_side2
                        command_response = "Rectangle's perimeter is %.2f and area is %.2f" % (perimeter, area)

                        if len(args) >= 3:
                            second_side = args[2]
                        else:
                            second_side = args[1]
                        logged_in_data = "   sides %s %s: %s" % (args[1], second_side, command_response)
                        solution_file = open(current_user_logged_in + "_solutions.txt", "a")
                        solution_file.write(logged_in_data + "\n")
                        solution_file.close()
                    except ValueError:
                        command_response = "Sides must be a integer NOT a string"
            else:
                command_response = "300 invalid command"

     # creating "LIST" command
        elif commands == "LIST":
            if not logged_in:
                command_response = "User not logged in, Please log in first."
            elif len(args) == 0:
                # creating a file that include the current user logged in solutions
                filename = current_user_logged_in + "_solutions.txt"
                if os.path.isfile(filename):
                    solution_file = open(filename, "r")
                    in_file_info = solution_file.read()
                    solution_file.close()
                else:
                    in_file_info = "   No content in the file yet\n"
                command_response = current_user_logged_in + "\n" + in_file_info
            elif args[0] == "-all":
                if current_user_logged_in != "root":
                    command_response = "Error: you are not the root user"
                else:
                    command_response = ""
                    for user in users_login:
                        filename = user + "_solutions.txt"
                        if os.path.exists(filename):
                            solution_file = open(filename, "r")
                            in_file_info = solution_file.read()
                            solution_file.close()
                        else:
                            in_file_info = "   No content in the file yet\n"
                        command_response = command_response + user + "\n" + in_file_info
            else:
                command_response = "300 invalid command"

        # Creating Logout command
        elif commands == "LOGOUT":
            # Once user types "LOGOUT" command response will display
            command_response = "200 OK"
            connect.send((command_response + "\n").encode())
            logged_in = False
            current_user_logged_in = None
            break   # exit the loop and allows the server to keeps running for next client

        # Creating ShutDown Command
        elif commands == "SHUTDOWN":
            command_response = "200 OK"
            connect.send((command_response + "\n").encode())
            shut_down = True
            break   # exits the loop, Server will shut down completely
        else:
            command_response = "300 invalid command"

        # Send the response (LOGOUT and SHUTDOWN already sent above and broke out)
        connect.send((command_response + "\n").encode())

    # Closing the client connection to the server
    connect.close()
    print("Client has been disconnected")

# Closing the server and exiting
s.close()
print("Server is shutting down")