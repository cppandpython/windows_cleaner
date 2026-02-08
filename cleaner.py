# CREATOR 
# GitHub https://github.com/cppandpython
# NAME: Vladislav 
# SURNAME: Khudash  
# AGE: 17

# DATE: 12.11.2025
# APP: WINDOWS_CLEANER
# TYPE: CLEANER
# VERSION: LATEST
# PLATFORM: win32


from os.path import join as joinp, exists, getsize
from subprocess import run as cmd, DEVNULL
from os import walk, mkdir, rmdir, remove
from sys import exit as _exit, executable
from shutil import get_terminal_size
from getpass import getuser
from ctypes import windll
from sys import platform


if platform != 'win32': 
    raise SystemError(f'DO NOT SUPPORTED ({platform})')

if windll.shell32.IsUserAnAdmin() == 0:
    windll.shell32.ShellExecuteW(None, 'runas', executable, __file__, None, 1)
    _exit()

USER = getuser()

# THESE PATHS WILL ALWAYS BE CLEARED
#------------------------------------#
PATHS_TO_CLEANING = [
    rf'C:\Users\{USER}\AppData\Local\Temp', 
    r'C:\Windows\Temp', 
    r'C:\Windows\SystemTemp', 
    r'C:\Windows\Logs'
]
#------------------------------------#

# THESE PATHS WILL ONLY BE CLEANED DURING DEEP CLEANING
#-------------------------------------------------------#
PATHS_TO_DEEP_CLEANING = [
    r'C:\Windows.old', 
    r'C:\Recovery',
    r'C:\Windows\$Windows.~WS', 
    r'C:\Windows\$Windows.~BT',
    r'C:\Windows\TempInst', 
    r'C:\Windows\CbsTemp', 
    r'C:\Users\Default\AppData\Local\Temp', 
    r'C:\ProgramData\Package Cache', 
    rf'C:\Users\{USER}\AppData\Local\Package Cache', 
    r'C:\ProgramData\Microsoft\Windows\Caches', 
    rf'C:\Users\{USER}\AppData\Local\Microsoft\Windows\Caches', 
    rf'C:\Users\{USER}\AppData\Local\Microsoft\Internet Explorer\CacheStorage', 
    rf'C:\Users\{USER}\AppData\Local\Microsoft\TokenBroker\Cache', 
    rf'C:\Users\{USER}\AppData\Local\Microsoft\Identity\Cache', 
    rf'C:\Users\{USER}\AppData\Local\Microsoft\Media Player\Transcoded Files Cache', 
    r'C:\Program Files (x86)\Google\GoogleUpdater\crx_cache', 
    r'C:\Windows\System32\Logs', 
    r'C:\Windows\System32\winevt\Logs', 
    r'C:\Windows\System32\wbem\Logs', 
    r'C:\Windows\SysWOW64\wbem\Logs',
    r'C:\Windows\security\logs', 
    r'C:\Windows\System32\DriverStore\Temp', 
    r'C:\Windows\Installer', 
    r'C:\Windows\Downloaded Program Files',
    r'C:\Windows\Prefetch', 
    r'C:\ProgramData\Microsoft\Windows\WER\Temp', 
    r'C:\ProgramData\Microsoft\Windows\WER\ReportArchive', 
    r'C:\Windows\LiveKernelReports', 
    r'C:\Windows\SoftwareDistribution\Download', 
    r'C:\Windows\ServiceProfiles\LocalService\AppData\Local\Microsoft\Windows\DeliveryOptimization', 
    rf'C:\Users\{USER}\AppData\Roaming\Adobe\Common', 
    rf'C:\Users\{USER}\AppData\Local\NVIDIA\GLCache'
]
#-------------------------------------------------------#


def _clear_directory(directory):
    global cleared_MB

    for _root, dirs, files in walk(directory, topdown=False):
        for _file in files: 
            _file = joinp(_root, _file)

            try:
                file_size = getsize(_file) / 1024 / 1024
            except:
                continue

            try: 
                remove(_file)
            except: 
                if exists(_file): 
                    for cmd_del_command in [
                        f'del /q /f "{_file}"', 
                        f'del /q /f /A:H "{_file}"', 
                        f'del /q /f /A:S "{_file}"'
                    ]:
                        if not exists(_file): 
                            break

                        cmd(cmd_del_command, stdout=DEVNULL, stderr=DEVNULL, shell=True)

            if not exists(_file): 
                cleared_MB += file_size
                print(f'File was removed --> {_file}')
        
        for _dir in dirs:
            dir_path = joinp(_root, _dir)

            try:
                rmdir(dir_path)
                print(f'Folder was removed --> {dir_path}')
            except:
                if exists(dir_path):
                    cmd(f'rmdir /q /s "{dir_path}"', stdout=DEVNULL, stderr=DEVNULL, shell=True)
                
                if not exists(dir_path):
                    print(f'Folder was removed --> {dir_path}')


def clear_directory(directory_path):
    if exists(directory_path):
        try: 
            _clear_directory(directory_path)
        except: 
            return


def start_cleaning(paths_clear_directory, paths_create_directory):
    for path_clear_directory in paths_clear_directory: 
        try: 
            clear_directory(path_clear_directory)
        except: 
            continue

    for path_create_directory in paths_create_directory: 
        try: 
            mkdir(path_create_directory)
        except: 
            continue 


def main():
    global cleared_MB

    shell_width = get_terminal_size()[0]
    cleared_MB = 0.0

    while True:
        try: 
            cmd('cls', shell=True)

            match input('Deep cleaning\nYes\\No: ').lower().strip():
                case 'exit': 
                    _exit()
                case 'yes': 
                    deep_flag = True
                case 'no':
                    deep_flag = False
                case _: 
                    continue
        except KeyboardInterrupt: 
            _exit()
        except: 
            continue
        else: 
            break

    cmd('cls', shell=True)

    left = (shell_width // 2) - 16
    right = (shell_width // 2) - 17

    print(f'/{"-":-^{left}}<Cleaning started successfully>{"-":-^{right}}\\')
    start_cleaning(PATHS_TO_CLEANING, PATHS_TO_CLEANING)
    
    if deep_flag: 
        start_cleaning(PATHS_TO_DEEP_CLEANING, PATHS_TO_DEEP_CLEANING[4:]) 
        
        for cmd_command in [
            'ipconfig /flushdns', 
            'wsreset', 
            'taskkill /f /IM WinStore.App.exe', 
            'Dism.exe /online /Cleanup-Image /StartComponentCleanup'
        ]:
            try: 
                cmd(cmd_command, stdout=DEVNULL, stderr=DEVNULL, shell=True)
            except:
                continue

    output_len = (
        len(f'<Cleaning completed successfully {round(cleared_MB, 1)} MB>'
        ) - len('<Cleaning started successfully>')
    ) // 2
    left = ((shell_width // 2) - 16) - (output_len + 1)
    right = ((shell_width // 2) - 17) - output_len

    input(
        f'/{"-":-^{left}}' + \
        '<Cleaning completed successfully ' + \
        f'{round(cleared_MB, 1)} MB>{"-":-^{right}}\\\n'
    )


main()