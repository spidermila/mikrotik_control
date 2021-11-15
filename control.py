import getpass

from cls import cls
from configuration import Configuration
from device import Device
from menu import Menu

def main() -> int:
    config = Configuration(getpass.getpass())
    config.check_or_create_config_file()
    config.load_config()
    
    main_menu_commands = {
        'quit cmnds': ['q', 'quit', 'exit'],
        'help cmnds': ['h', 'help'],
        'list cmnds': ['l', 'list'],
        'create cmnds': ['c', 'create'],
    }
    main_menu = Menu(config, main_menu_commands)
    
    # TODO: zkontrolovat, jestli existuje cfg.yaml
    # TODO: zkontrolovat, jestli ma cfg.yaml minimalni interni strukturu

    cls()
    while main_menu.run():
        ...
        

if __name__ == '__main__':
    raise SystemExit(main())