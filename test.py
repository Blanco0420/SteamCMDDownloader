import subprocess

# Define the command and string to check for
command = ['steamcmd', '+login', 'username']
check_string = 'password:'

# Start the process with stdout and stderr piped
with subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as process:
    while True:
        output = process.stdout.readline()
        error = process.stderr.readline()
        
        # Output might be empty at the end, so check for both
        if output == '' and error == '' and process.poll() is not None:
            break
        
        # Print stdout
        if output:
            print(output, end='')

        # Print stderr
        if error:
            print(error, end='')

        # Check for the specific string in stdout
        if check_string in output:
            print(f'Found "{check_string}" in output: {output.strip()}')

        # Check for the specific string in stderr
        if check_string in error:
            print(f'Found "{check_string}" in error: {error.strip()}')

        # Example for checking a password prompt and sending a password (uncomment if needed)
        # if 'password' in output.lower() or 'password' in error.lower():
        #     process.stdin.write('your_password\n')
        #     process.stdin.flush()
