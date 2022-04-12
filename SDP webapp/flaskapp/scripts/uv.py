#Controls the UV light of the robot, supposed to be run as - python uv.py ON or python uv.py OFF from ssh.py
import sys
from paul_pi import Paul
STATE = sys.argv[1]
paul = Paul()
if STATE == 'ON':
    paul.light_on()
if STATE == 'OFF':
    paul.light_off()

