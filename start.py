import subprocess
import argparse

parser = argparse.ArgumentParser(description='Start the application')
parser.add_argument('--ip', type=str, default='localhost', help='IP to run the application on')
parser.add_argument('--port', type=int, default=5000, help='Port to run the application on')
parser.add_argument('--debug', action='store_true', help='Run the application in debug mode')
parser.add_argument('--HI', action='store_true', help='Run the application with the Hardware Interface')
parser.add_argument('--MP', action='store_true', help='Run the application with the Movement Package')
parser.add_argument('--CP', action='store_true', help='Run the application with the Camera Package')
parser.add_argument('--AI', action='store_true', help='Run the application with the AI Package')
parser.add_argument('--SP', action='store_true', help='Run the application with the Sonar Package')
parser.add_argument('--all', action='store_true', help='Run the application with all packages')
args = parser.parse_args()

commands = [
    ['python3', 'src/FlaskServer.py', '--ip', str(args.ip), '--port', str(args.port)],
    ['python3', 'src/HardwareInterface.py', '--ip', str(args.ip), '--port', str(args.port)],
    ['python3', 'src/MovementPackage.py', '--ip', str(args.ip), '--port', str(args.port)],
    ['python3', 'src/CameraPackage.py', '--ip', str(args.ip), '--port', str(args.port)],
    ['python3', 'src/AIPackage.py', '--ip', str(args.ip), '--port', str(args.port)],
    ['python3', 'src/SonarPackage.py', '--ip', str(args.ip), '--port', str(args.port)]
]

processes = []

if args.all:
    print('Running all packages')
    if args.debug:
        for i in range(0, len(commands)):
            processes.append(subprocess.Popen(commands[i] + ['--debug']))
    else:
        for i in range(0, len(commands)):
            processes.append(subprocess.Popen(commands[i]))
elif args.HI:
    print('Running Hardware Interface')
    if args.debug:
        processes.append(subprocess.Popen(commands[1] + ['--debug']))
    else:
        processes.append(subprocess.Popen(commands[1]))
elif args.MP:
    print('Running Movement Package')
    if args.debug:
        processes.append(subprocess.Popen(commands[2] + ['--debug']))
    else:
        processes.append(subprocess.Popen(commands[2]))
elif args.CP:
    print('Running Camera Package')
    if args.debug:
        processes.append(subprocess.Popen(commands[3] + ['--debug']))
    else:
        processes.append(subprocess.Popen(commands[3]))
elif args.AI:
    print('Running AI Package')
    if args.debug:
        processes.append(subprocess.Popen(commands[4] + ['--debug']))
    else:
        processes.append(subprocess.Popen(commands[4]))
elif args.SP:
    print('Running Sonar Package')
    if args.debug:
        processes.append(subprocess.Popen(commands[5] + ['--debug']))
    else:
        processes.append(subprocess.Popen(commands[5]))
if not args.all:
    print('Running Flask Server')
    if args.debug:
        processes.append(subprocess.Popen(commands[0] + ['--debug']))
    else:
        processes.append(subprocess.Popen(commands[0]))

while True:
    try:
        for process in processes:
            process.wait()
    except KeyboardInterrupt:
        for process in processes:
            process.kill()
        break
