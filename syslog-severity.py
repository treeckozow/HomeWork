import subprocess

def run_local_command(command):
    try:
        # Run the command
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout, result.stderr

    except subprocess.CalledProcessError as e:
        print(f"Command '{command}' returned non-zero exit status {e.returncode}")
        print(f"Error output: {e.stderr}")

timestamp = run_local_command("date +%s")[0].strip()
warn_num = run_local_command('grep -ic "warn" /var/log/syslog')[0].strip()
error_num = run_local_command('grep -ic "error" /var/log/syslog')[0].strip()
info_num = run_local_command('grep -ic "info" /var/log/syslog')[0].strip()

data = {"timestamp": timestamp, "Info": info_num, "Warn": warn_num, "Error": error_num}

print(timestamp)
print(info_num)
print(warn_num)
print(error_num)


