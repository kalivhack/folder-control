#!/usr/bin/env python
import os
import sys
import argparse
import json
import datetime

from typing import (Never, TextIO)
from getpass import getuser
from time import sleep

import classes

def parse_args() -> dict:
    parser = argparse.ArgumentParser()
    platforms = {
        'nt': rf'C:/Users/{getuser()}/Downloads',
        'posix': rf'/home/{getuser()}/Downloads'
    }

    default_path = os.name

    parser.add_argument('-p', '--path', help='The Path Of Folder To Control',
                        default=platforms.get(os.name), dest='path', required=False)
    parser.add_argument('-b', '--background', help='Activate Background Mode',
                        dest='bg', default=False, action="store_true", required=False)

    return parser.parse_args().__dict__


def sort_files(folder_path: str, extensions: dict, *, output_loc: TextIO = sys.stdout) -> Never:
    now_time = datetime.datetime.now().strftime('%d:%m:%y')
    os.chdir(folder_path)
    
    while True:
        files = os.listdir()

        for file in files:
            # Ignoring Directory or .crdownload File
            if file.endswith('crdownload') or os.path.isdir(file):
                continue

            # Convertng File Extension to Folder Name
            moving_folder = extensions.get(file.split('.')[-1], 'Other')
            
            # Making Folder With That Name If That Don't Exist
            if not os.path.exists(f"{folder_path}/{moving_folder}"):
                print(f'[{now_time}] [ + ] Folder {moving_folder} Created In {folder_path}.', file=output_loc)
                os.mkdir(moving_folder)

            os.replace(file, f'{moving_folder}/{file}')
            print(f'[{now_time}] [ + ] File {file} Was Successfully Moved To {folder_path}/{moving_folder}', file=output_loc)
                
        sleep(5)


if __name__ == '__main__':
    path, bg_mode = parse_args().values()
    curr_dir = os.getcwd()

    moving_location = sys.stdout

    if bg_mode:
        moving_location = classes.loger(f'{curr_dir}\\log\\{datetime.datetime.now():%d_%m_%Y}.txt')
    
    try:
        with open('src/categories.json', 'r') as extensions_file:
            extensions = json.load(extensions_file)

        sort_files(path, extensions, output_loc=moving_location)

    except KeyboardInterrupt:
        exit(f'\n[{datetime.datetime.now():%H:%M:%S}] [ - ] Ctrl+C Detected. Exiting...\n')
    
    except BaseException as ex:
        exit(f"\n{ex}\n")

    finally:
        moving_location.close()