from configuration import Configuration
from create_dialog import Create_Dialog

class Menu:
    def __init__(self, config: Configuration, commands: dict) -> None:
        self.commands = commands
        self.config = config

    def run(self):
        command_line = input(': ')
        if len(command_line) > 0:
            command = command_line.lower().split()[0]
            if command in self.commands['quit cmnds']:
                return 0
            elif command in self.commands['help cmnds']:
                for c in self.commands:
                    print(f'{c}: {self.commands[c]}')
            elif command in self.commands['list cmnds']:
                if len(self.config.targets) > 0:
                    if self.config.is_password_correct(self.config.targets[0]['password']):
                        for device in self.config.targets:
                            print(f'nme: {device["name"]}')
                            print(f'IPa: {device["address"]}')
                            print(f'prt: {device["port"]}')
                            print(f'usr: {device["user"]}')
                            print('-'*20)
                    else:
                        print("Wrong password. Can't decrypt passwords for the devices.")
            elif command in self.commands['create cmnds']:
                create_dialog = Create_Dialog(self.config)
                create_dialog.run()
            else:
                print('Unknown command')
                print('')