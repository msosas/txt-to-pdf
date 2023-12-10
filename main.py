from loguru import logger
from pdf import generate
import argparse
import os


def get_absolute_file_paths(directory_path):
    absolute_paths = set()
    for foldername, _, filenames in os.walk(directory_path):
        for filename in filenames:
            file_path = os.path.join(foldername, filename)
            absolute_paths.add(os.path.abspath(file_path))
    return absolute_paths


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert .txt music tab files into PDFs. Provide the path of your tabs and a destination folder')
    parser.add_argument('--input','-i', help='Directory where the txt files are', required=True)
    parser.add_argument('--output','-o', help='Directory where pdf will be saved', required=True)
    args = vars(parser.parse_args())

    tab_files = get_absolute_file_paths(args['input'])
    for file in tab_files:
        try:
            file_name = file.replace(f'{args["input"]}/','')
            generate(file, f'{args["output"]}/{file_name}')
        except Exception as e:
            logger.error(f'{file_name}:{e}')
