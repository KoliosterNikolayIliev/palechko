import os


def clean_up_files(path):
    try:
        os.remove(path)
    except:
        print('file does not exists')
