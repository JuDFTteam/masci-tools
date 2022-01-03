"""
Function to collect input files from a specfied folder and subfolders and copy them to
the tests/files/fleur folder
"""
import os
import sys
import shutil

CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))


def collect_fleur_xml_files(*args):
    base_folders = [x for i, x in enumerate(args[0]) if i % 2 == 1]
    test_folders = [x for i, x in enumerate(args[0]) if i % 2 == 0]
    for orig, dest, in zip(base_folders, test_folders):
        dest_folder = os.path.join(CURRENT_DIRECTORY, dest)
        for root, dirs, files in os.walk(orig):
            for file in files:
                if file.endswith('.xml'):
                    copyfrom = os.path.join(root, file)
                    rel_path = copyfrom.replace(orig + '/', '')
                    copyto = os.path.join(dest_folder, rel_path)
                    if '/work/' in copyto:
                        copyto = copyto.replace('/work/', '/files/')
                    print(f'Copying {copyfrom}')
                    os.makedirs(os.path.dirname(copyto), exist_ok=True)
                    shutil.copy(copyfrom, copyto)


if __name__ == '__main__':
    collect_fleur_xml_files(sys.argv[1:])
