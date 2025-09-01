import ebooklib
from ebooklib import epub
import cmd

# Accept arg with path to epub to extract
class command_line(cmd.Cmd):
    def __init__(self):
        super().__init__()
        self.prompt = 'epub-extractor> '

    def do_extract(self, arg):
        'Extract images from the specified EPUB file: extract <path_to_epub>'
        try:
            book = epub.read_epub(arg)
            for image in book.get_items_of_type(ebooklib.ITEM_IMAGE):
                print(f'Extracted image: {image.get_name()}')
        except Exception as e:
            print(f'Error: {e}')

    def do_exit(self, arg):
        'Exit the command line interface'
        return True
