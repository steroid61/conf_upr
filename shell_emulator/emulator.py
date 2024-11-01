import os
import tarfile
import xml.etree.ElementTree as ET
from xml.dom import minidom
import datetime
import shutil
class ShellEmulator:
    def __init__(self, config_path):
        self.load_config(config_path)
        self.current_path = '/'
        self.clear_log()

    def clear_log(self):
        with open(self.log_path, 'w') as f:
            f.write('<log></log>')

    def load_config(self, config_path):
        tree = ET.parse(config_path)
        root = tree.getroot()
        self.username = root.find('username').text
        self.vfs_path = root.find('vfs_path').text
        self.log_path = root.find('log_path').text
        self.startup_script = root.find('startup_script').text
        self.extract_vfs()

    def extract_vfs(self):
        with tarfile.open(self.vfs_path, 'r') as tar:
            tar.extractall(path='vfs')

    def log_command(self, command):
        entry = ET.Element('entry')
        user_elem = ET.SubElement(entry, 'user')
        user_elem.text = self.username
        command_elem = ET.SubElement(entry, 'command')
        command_elem.text = command
        timestamp_elem = ET.SubElement(entry, 'timestamp')
        timestamp_elem.text = datetime.datetime.now().isoformat()

        if os.path.exists(self.log_path):
            tree = ET.parse(self.log_path)
            root = tree.getroot()
            root.append(entry)
        else:
            root = ET.Element('log')
            root.append(entry)

        xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="    ")
        xml_str = "\n".join(line for line in xml_str.splitlines() if line.strip())
        with open(self.log_path, 'w') as f:
            f.write(xml_str)

    def ls(self):
        files = os.listdir('vfs' + self.current_path)
        for f in files:
            print(f)
        self.log_command('ls')

    def cd(self, path):
        new_path = os.path.join(self.current_path, path)
        if os.path.isdir('vfs' + new_path):
            self.current_path = new_path
        else:
            print(f"No such directory: {path}")
        self.log_command(f'cd {path}')

    def cp(self, src, dest):
        if os.path.isdir(dest):
            src_path = 'vfs' + os.path.join(self.current_path, src)
            dest_path= dest
            if os.path.isfile(src_path):
                shutil.copy(src_path, dest_path)
                print(f"Copied {src} to {dest}")
            else:
                print(f"No such file: {src}")
        else:
            if dest.find('/')==-1:
                src_path ='vfs'+os.path.join(self.current_path, src)
                dest_path ='vfs'+os.path.join(self.current_path, dest)
                # cd привет/документы
                # cp документ.txt документ1.txt
                if os.path.isfile(src_path):
                    shutil.copy(src_path, dest_path)
                    print(f" {src} is copied with name {dest}")
                else:
                    print(f"No such file: {src}")
            else:
                print(f"No such directory: {dest}")
        self.log_command(f'cp {src} {dest}')

    def date(self):
        print(datetime.datetime.now())
        self.log_command('date')

    def run_command(self, command):
        parts = command.split()
        cmd = parts[0]
        if cmd == 'ls':
            self.ls()
        elif cmd == 'cd' and len(parts) > 1:
            self.cd(parts[1])
        elif cmd == 'cp' and len(parts) > 2:
            self.cp(parts[1], parts[2])
        elif cmd == 'date':
            self.date()
        elif cmd == 'exit':
            exit()
        else:
            print(f"Unknown command: {cmd}")

    def run(self):
        if os.path.exists(self.startup_script):
            with open(self.startup_script) as f:
                for line in f:
                    self.run_command(line.strip())

        while True:
            command = input(f"{self.username}@shell:{self.current_path}$ ")
            self.run_command(command)


if __name__ == '__main__':
    emulator = ShellEmulator('config.xml')
    emulator.run()
