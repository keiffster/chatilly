
from textfiles import TextFileProcessor


class DuplicateRemover(TextFileProcessor):

    @staticmethod
    def get_title():
        return 'AIML Duplicate Remover Text File Processor'

    def _process_line(self, line, args):
        if line.startswith ("DUPLICATE:"):
            print("[%s]"%line.strip())
 
 
if __name__ == '__main__':

    processor = DuplicateRemover()
    parser = processor.create_base_args_parser()

    args = parser.parse_args()

    if processor.process(args) is False:
        parser.print_help()
        print("\n")
    