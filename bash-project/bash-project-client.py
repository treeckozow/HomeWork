from SshToServer import SshToServer

def getCommandOutput(command):
    stdout, stderr = my_ssh.runRemoteCommand(command)
    if stderr != "":
        return "Error: " + stderr
    return stdout

my_ssh = SshToServer(r"C:\Users\treec\Desktop\forward\AWS\keypair-1.pem", "16.16.63.19", "ubuntu")

file_name = input("Please enter the name of the file: ")
waiting_time = input("How many seconds to wait? ")

print(getCommandOutput(f"./bash-project-server.sh {file_name} {waiting_time}").strip())