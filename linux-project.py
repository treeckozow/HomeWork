from SshToServer import SshToServer
import pandas as pd
import os

def getCommandOutput(command):
    stdout, stderr = my_ssh.runRemoteCommand(command)
    if stderr != "":
        return "Error: " + stderr
    return stdout

def addToCsv(data, csv_path):
    new_dataframe = pd.DataFrame(data)
    if os.path.isfile(csv_path):
        current_dataframe = pd.read_csv(csv_path)
        dataframe = pd.concat([current_dataframe, new_dataframe], ignore_index=True)
    else:
        dataframe = new_dataframe
    dataframe.to_csv(csv_path, index=False)

path = r"C:\Users\treec\Desktop\forward\Linux\logs-stats.csv"
my_ssh = SshToServer(r"C:\Users\treec\Desktop\forward\AWS\keypair-1.pem", "16.16.63.19", "ubuntu")

ssh_output = getCommandOutput("python3 syslog-severity.py").split()
severity_data = [
    {"Timestamp": ssh_output[0], "Info": ssh_output[1], "Warn": ssh_output[2], "Error": ssh_output[3]}
]

addToCsv(severity_data, path)

