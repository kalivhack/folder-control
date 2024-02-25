#!/usr/bin/env python
import os
import sys
import argparse
import json
import datetime

from typing import Never
from getpass import getuser
from time import sleep


def parse_args() -> dict:
    """_summary_: Just Parsing Arguments

    Returns:
        dict: Returns Arguments In Dictionary
    """
    parser = argparse.ArgumentParser()

    platforms = {
        'nt': rf'C:/Users/{getuser()}/Downloads',
        'posix': rf'/home/{getuser()}/Downloads'
    }

    parser.add_argument('-p', '--path', help='The Path Of Folder To Control',
                        default=platforms.get(os.name), dest='path', required=False)
    parser.add_argument('-l', '--log', help='Activate Logging Mode (sys.stdout to log file)',
                        dest='bg', action='store_true', default=False, required=False)

    return parser.parse_args().__dict__


def sort_files(folder_path: str, extensions: dict) -> Never:
    """
    _summary_: Move Files In Folders By Thair Extensions 

    Args:
        folder_path (str): The Path Of Folder Where Fuction'll Sort Files
        extensions (dict): Function'll Use To Make Folder And Move File Inside With Given Extension

    Returns:
        Never: Function Never Returns Somethings

    Examples: 
        test.txt => Text/test.txt
        test.mp4 => Videos/test.mp4
        test.png => Pictures/test.png
    """
    os.chdir(folder_path)

    while True:
        now_time = datetime.datetime.now().strftime('%d/%m/%y - %H:%M')
        files = os.listdir()

        for file in files:
            # Ignoring Directory or .crdownload File
            if file.endswith('crdownload') or os.path.isdir(file):
                continue

            # Convertng File Extension to Folder Name
            moving_folder = extensions.get(file.split('.')[-1], 'Other')

            # Making Folder With That Name If That Don't Exist
            if not os.path.exists(f"{folder_path}/{moving_folder}"):
                print(
                    f'[{now_time}] [ + ] Folder "{moving_folder}" Created In {folder_path}.')
                os.mkdir(moving_folder)

            os.replace(file, f'{moving_folder}/{file}')
            print(
                f'[{now_time}] [ + ] File "{file}" Was Successfully Moved To {folder_path}/{moving_folder}')

        sys.stdout.flush()
        sleep(5)


if __name__ == '__main__':
    path, bg_mode = parse_args().values()
    
    if bg_mode:
        sys.stdout = open(f'{os.getcwd()}\\log\\{
                          datetime.datetime.now():%d_%m_%Y}.log', 'w')

    try:
        with open('src/categories.json', 'r') as extensions_file:
            extensions = json.load(extensions_file)

        sort_files(path, extensions)

    except KeyboardInterrupt:
        exit(
            f'\n[{datetime.datetime.now():%H:%M:%S}] [ - ] Ctrl+C Detected. Exiting...\n')

    except BaseException as ex:
        exit(f"\n{ex}\n")

    finally:
        sys.stderr.flush()
        sys.stdout.close()
