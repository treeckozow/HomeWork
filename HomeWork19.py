from SshToServer import SshToServer

my_ssh = SshToServer(r"C:\Users\treec\Desktop\forward\AWS\keypair-1.pem", "16.16.63.19", "ubuntu")

def getCommandOutput(ssh):
    user_command = input("Command: ")
    stdout, stderr = ssh.runRemoteCommand(user_command)
    if stderr != "":
        return "Error: " + stderr
    return stdout

if __name__ == "__main__":
    output = getCommandOutput(my_ssh)
    print(output)