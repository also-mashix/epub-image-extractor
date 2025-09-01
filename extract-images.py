
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

    # Accept arg with path to epub to extract and extract images
    def do_extract(self, arg):
        'Extracted images will be saved to: <epub-file-name>_images directory'
        
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
        
        # Create image folder
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        # Open ebook, find images, save to directory
        try:
            book = epub.read_epub(arg)
            for image in book.get_items_of_type(ebooklib.ITEM_IMAGE):
                image_path = os.path.join(dir_path, image.get_name())
                with open(image_path, 'wb') as img_file:
                    img_file.write(image.get_content())
                print(f'Saved image: {image.get_name()} to {dir_path}')
        except Exception as e:
            print(f'Error: {e}')

    def do_exit(self, arg):
        'Exit the command line interface'
        return True
