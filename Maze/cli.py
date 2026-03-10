import argparse

def get_file_path():
    parser = argparse.ArgumentParser(description="Enter the path to the Labyrinth file!")
    parser.add_argument('-f', '--file', metavar='Labyrinth file path',
                        help="The Labyrinth from the file at the passed in path will be used as the Labyrinth.")
    args = parser.parse_args()
    
    return args.file