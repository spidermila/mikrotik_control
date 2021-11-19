from os import system
from sys import platform

def cls() -> None:
    if platform.find('linux') != -1:
        cls_command = 'clear'
    elif platform.find('win') != -1:
        cls_command = 'cls'
    elif platform.find('darwin') != -1:
        cls_command = 'clear'
    else:
        print('Unknown OS. cls will not work!')
        cls_command = False # type: ignore
    if cls_command: system(cls_command)
