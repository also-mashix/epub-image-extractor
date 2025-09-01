import ebooklib
from ebooklib import epub
import cmd
import os
import shutil

# Accept arg with path to epub to extract
class command_line(cmd.Cmd):
    def __init__(self):
        super().__init__()
        # Set the command prompt to indicate the tool is active
        self.prompt = 'epub-extractor> '

    def preloop(self):
        print("Please paste the full path to an epub file.")
        print("Type: exit to quit.")

    def default(self, line):
        # Remove surrounding quotes if present
        line = line.strip().strip('"').strip("'")
        # Try to extract if the input looks like a file path
        if os.path.isfile(line) and line.lower().endswith('.epub'):
            self.do_extract(line)
        else:
            print(f'*** Unknown syntax: {line}')

    # Accept arg with path to epub to extract and extract images
    def do_extract(self, arg):
        # Remove surrounding quotes if present
        arg = arg.strip().strip('"').strip("'")
        
        print(f'Extracted images will be saved to: <epub-file-name>_images directory')
        
        # input validation
        if not arg:
            print('Error: No epub file path provided.')
            return  
        if not os.path.isfile(arg):
            print('Error: Provided path is not a valid file.')
            return
        if not arg.lower().endswith('.epub'):
            print('Error: Provided file is not an epub.')
            return
        
        # Image folder name
        dir_path = arg[:-5] + '_images'
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path) # Remove existing directory
            print(f'log)  removed existing directory: {dir_path}')
        
        # Create image folder
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print(f'log)  made directory: {dir_path}')

        # Open ebook, find images, save to directory
        try:
            book = epub.read_epub(arg)
            for image in book.get_items_of_type(ebooklib.ITEM_IMAGE):
                image_path = os.path.join(dir_path, image.get_name().split('/')[1])
                with open(image_path, 'wb') as img_file:
                    img_file.write(image.get_content())
                print(f'Saved image: {image.get_name()} to {dir_path}')
        except Exception as e:
            print(f'Error: {e}')

    def do_exit(self, arg):
        'Exit the command line interface'
        return True

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        cli = command_line()
        cli.do_extract(sys.argv[1])
    else:
        command_line().cmdloop()