import os
import json

from getpass import getuser

if __name__ == '__main__':
    answer = input('This Script Will Create ~250 Files For Testing. Do You Agree (y/n): ')

    if answer.lower() == 'y':
        path = './test/'
        
        if not os.path.exists(path):
            os.makedirs(path)
            
        # Loading Extensions
        with open('src/categories.json', 'r') as read_file:
            extensions = json.load(read_file)

        # Changing Directory
        os.chdir(path)

        counter = 0

        for name, extension in extensions.items():
            os.open("%s.%s"%(extension, name), flags=os.O_CREAT)
            counter += 1

        print(f"{counter} Files Was Created.")
    
    print('Bye...')
