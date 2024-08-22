import subprocess
import os

class PackageInstaller:
    def __init__(self, install: bool = False, debug: bool = False):
        self.install = install
        self.debug = debug

        # Check if 'requirements.txt' exists in the current working directory
        if os.path.exists(os.path.join(os.getcwd(), 'requirements.txt')):
            self.requirements = os.path.join(os.getcwd(), 'requirements.txt')
        else:
            self.requirements = None  # Set to None if the file doesn't exist
        
    def installPackages(self):
        if self.install:
            try:
                if self.requirements:
                    subprocess.run(['pip3', 'install', '-r', self.requirements])
                else:
                    print("requirements.txt not found.")
            except Exception as e:
                print(e)
                return False
        return True

if __name__ == '__main__':
    installer = PackageInstaller(install=True, debug=True)
    installer.installPackages()
