# API for flask app used for establishing an ssh connection to the Pi via the DICE command line and running scripts
import paramiko
from scp import SCPClient
import sys

class ssh():
    def __init__(self):
        ''' Initializes the SSH Client and establish an ssh connection to the Raspberry Pi using the 
            IP, username and password of the Pi '''
            
        # IP address of the Pi we are connecting to 
        self.IP = 'pikachu'
        # Username of the Pi
        self.username = 'pi'
        # Password of the Pi
        self.password = 'r00t'
        # Initialising the ssh client using the paramiko library
        self.client = paramiko.SSHClient()
        self.client.load_system_host_keys()
        # Establishing a connection to the Raspberry Pi
        self.client.connect(self.IP,username=self.username,password=self.password)

    def execute_command(self,cmd):
        ''' Used to execute command line arguments from a script
            We use it to run our scripts'''

        print(f"Executing {cmd}")
        stdin_, stdout_, stderr_ = self.client.exec_command(cmd)
        status = stdout_.channel.recv_exit_status()
        print(f"STATUS {status}")
        for line in stdout_.readlines():
            print(line)
        if status != 0:
            errors = "\n".join(list(stderr_.readlines))
            raise Exception(f"{cmd} failed with {errors}")

    def progress4(self,f, size, sent, p):
        ''' Used to check the progress of the SCP file transfer to the Raspberry Pi in case
            we want to transfer a file '''

        prog = sent / size * 100.
        sys.stdout.write(f"({p[0]}:{p[1]}) {f}\'s progress: {prog}\r")

    def scp_file(self,local_path,remote_path):
        ''' Calls the SCP client to transfer a file to the Raspberry Pi, uses the progress4 function
            :param local_path - The directory in which we have the file
            :param remote_path - The directory inside the Pi in which we want to SCP the file'''

        with SCPClient(self.client.get_transport(),progress4 = self.progress4) as scp:
            scp.put(local_path, remote_path=remote_path)

    def kill_auto_mode(self):
        ''' Function to be called every time before run_auto_mode needs to be called.
            It terminates auto-mode.py'''
        
        self.execute_command(f"pkill -f auto-mode.py")

    def run_auto_mode(self,runtime, state):
        ''' Function to be called when user clicks on AUTO-MODE - ON or OFF and chooses the duration for which 
            drone is to be run. The auto-mode.py script is run using the execute_command function, passing 
            RUNTIME/DURATION and ON or OFF as an argument 
            :param runtime - Duration for which robot is supposed to run
            :param state - Decides ON/OFF for auto-mode.py
            :& - Ensures that after execution of command, terminal won't be occupied'''

        # On executing '&' at the end the terminal will no longer be occupied and can run other scripts.
        self.execute_command(f"python /home/pi/paul/auto-mode.py {runtime} {state} &") 

    def uv_on_off(self,light):
        ''' Function to be called when user clicks on UV-Mode - ON or UV-Mode - OFF
            Runs uv.py using execute_command, passing ON or OFF as the argument
            :param light - Decides ON/OFF for uv.py'''

        self.execute_command(f"python /home/pi/paul/uv.py {light}") 