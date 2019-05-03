
from files import FileProcessor


class TextFileProcessor(FileProcessor):

    @staticmethod
    def get_title():
        return 'AIML Text File Processor'

    def _process_line(self, line, args):
        if args.verbose:
            print("\t[%s]"%line)
        # Do nothing, return line as is
        return None

    def _process_lines(self, inputfilename, args):
        lines = []
        with open(inputfilename, "r+") as inputfile:
            for line in inputfile:
                new_line = self._process_line(line, args)
                if new_line:
                    lines.append()
        
        return lines

    def _process_file(self, inputfilename, outputfilename, args):
        print("Converting [%s] -> [%s]"%(inputfilename, outputfilename))
        lines = self._process_lines(inputfilename, args)
        self._write_outputfile(lines, outputfilename, args)

    def _write_outputfile(self, lines, outputfilename, args):
        print("Writing output file [%s]"%outputfilename)


if __name__ == '__main__':

    processor = TextFileProcessor()
    parser = processor.create_base_args_parser()

    args = parser.parse_args()

    if processor.process(args) is False:
        parser.print_help()
        print("\n")
    