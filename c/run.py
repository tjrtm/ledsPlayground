import subprocess

executable_path = '/home/tjrtm/shared/ledsPlayground/c/chase_smooth'
arguments = ['0x00FF00', '0']  
command = [executable_path] + arguments
result = subprocess.run(command, capture_output=True, text=True)
if result.returncode == 0:
    print("Execution successful.")
    print("Output:")
    print(result.stdout)
else:
    print("Execution failed.")
    print("Error:")
    print(result.stderr)
