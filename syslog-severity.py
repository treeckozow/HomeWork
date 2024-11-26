import subprocess

def run_local_command(command):
    try:
        # Run the command
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout, result.stderr

    except subprocess.CalledProcessError as e:
        print(f"Command '{command}' returned non-zero exit status {e.returncode}")
        print(f"Error output: {e.stderr}")

severity = [0] * 4
severity[0] = run_local_command("date +%s")[0].strip()

with open("/var/log/syslog") as syslog_file:
    syslog_list = syslog_file.readlines()

for line in syslog_list:
    if "info" in line.lower():
        severity[1] += 1
    if "warn" in line.lower():
        severity[2] += 1
    if "error" in line.lower():
        severity[3] += 1

for stat in severity:
    print(stat)

