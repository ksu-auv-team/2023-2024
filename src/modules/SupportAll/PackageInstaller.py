import subprocess
import os

class PackageInstaller:
    def __init__(self, install: bool = False, debug: bool = False):
        self.install = install
        self.debug = debug
        
        if os.path(os.path.join(os.getcwd(), 'requirements.txt')):
            self.requirements = os.path.join(os.getcwd(), 'requirements.txt')
        
    def installPackages(self):
        if self.install:
            try:
                if self.requirements:
                    subprocess.run(['pip3', 'install', '-r', self.requirements])
            except Exception as e:
                print(e)
                return False
        return True

                
        