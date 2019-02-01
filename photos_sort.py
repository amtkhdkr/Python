import os, shutil
from datetime import datetime

def main(path, new_path):
    count = 0
    for root, dirs, files in os.walk(path):
        for f in files:
            modified_time = datetime.fromtimestamp(os.stat(os.path.join(root, f)).st_mtime)
            if modified_time.hour < 12:
                hour_range = f'{modified_time:%I}{modified_time:%p} - {modified_time.hour+1}{modified_time:%p}'
            else:
                hour_range = f'{modified_time:%I}{modified_time:%p} - {modified_time.hour - 11}{modified_time:%p}'
            correct_path = os.path.join(new_path, f'{modified_time.day} Jan', hour_range)
            if not os.path.exists(correct_path): os.makedirs(correct_path)
            shutil.move(f'{root}\\{f}', f'{correct_path}\\{f}')
            count = count + 1
    print('Moved', count, 'photos')

if __name__ == '__main__':
    path = 'full_source_directory'
    new_path = 'full_destination_directory. will be created if does not exist'
    main()
