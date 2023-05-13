
import paramiko
import datetime
import zipfile
import subprocess
import os
import shutil

# Set up SSH client
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Load private key
private_key_file = 'your_private_key_path'
private_key = paramiko.RSAKey.from_private_key_file(private_key_file)

# Connect to Linux machine using private key
ssh.connect('your_id', username='your_username', pkey=private_key)

today = datetime.datetime.now()
yesterday = today - datetime.timedelta(days=9)
folder_name = yesterday.strftime("%Y%m%d")

sftp_command = f"echo 'ls\ncd your_folder_name\ncd your_foldername/{folder_name}\nget your_foldername_{folder_name}.zip\nls' | sftp -P your_port -i your_private_key your_user_name@your_id"

# Execute command
stdin, stdout, stderr = ssh.exec_command(sftp_command)
stdout.read().decode()

# Define the command to execute
command = f"scp -i your_private_key_path your_user_name@your_id:your_folder_path_{folder_name}.zip your_path_to_save"

# Execute the command and capture the output
result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

# Check the return code to see if the command was successful
if result.returncode == 0:
    print("Command executed successfully!")
else:
    print(f"An error occurred:\n{result.stderr.decode('utf-8')}")

# Close connection
ssh.close()

with zipfile.ZipFile(f'_your_filepath_{folder_name}.zip', 'r') as zip_ref:
    zip_ref.extractall('your_filepath_to_extract')

# Delete the zip file
os.remove(f'your_filepath_to_delete_{folder_name}.zip')
