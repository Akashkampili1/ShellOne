# ShellOne - Reverse Shell Generator

ShellOne is a Python script for generating PHP reverse shells that can be used to establish a connection to a remote server. This tool is designed for educational and ethical hacking purposes to gain remote access to a target server, provided that you have appropriate permissions.


## Installation

1. Clone the repository to your local machine using [Git](https://git-scm.com/):

   ```bash
   git clone https://github.com/your-username/ShellOne.git

2.Navigate to the project directory:

    cd ShellOne

3. Run the Python script by providing the required input (IP address, port number, and file name):

    python3 shellone.py


## Usage

1. Run the script and provide the IP address, port number, and the desired file name for the PHP code.
2. The script will generate the PHP code and save it with the specified file name.
3. Follow the instructions below to establish a Netcat listener and gain remote access to the target server.

## Instructions

1. Open a terminal and navigate to the directory containing the generated PHP file.

2. Start a Netcat listener on the specified port:


3. Execute the generated PHP code on the target server.

4. After executing the PHP code, you should have a reverse shell connection to the target server.

5. You can upgrade the shell to a more interactive one using the following command:

## Command to Upgrade the shell

python -c 'import pty; pty.spawn("/bin/bash")'
