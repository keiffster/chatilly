import os
import re
import sys
import xml.etree.ElementTree as ET
import argparse

class FileProcessor(object):

    @staticmethod
    def get_title():
        return 'AIML Utilities'

    def create_base_args_parser(self):
        parser = argparse.ArgumentParser(description=self.get_title())
        
        parser.add_argument('-if', '--inputfile', action="store", dest="inputfile", help="Input file")
        parser.add_argument('-of', '--outputfile', action="store", dest="outputfile", help="Output file")
        parser.add_argument('-id', '--inputdir', action="store", dest="inputdir", help="Input dir")
        parser.add_argument('-od', '--outputdir', action="store", dest="outputdir", help="Output dir")

        parser.add_argument('-verbose', action="store", dest="verbose", default=False, help="Verbose output")
        parser.add_argument('-dummy', action="store", dest="dummy", default=False, help="Don't modify output file(s)")

        return parser

    def process(self, args):
        if args.inputfile and args.outputfile:
            return self.process_single_file(args)

        elif args.inputdir and args.outputdir:
            return self.process_folders(args)

        return False

    def _process_file(self, inputfile, outputfile, args):
        print("Converting [%s] -> [%s]"%(inputfile, outputfile))

    def process_single_file(self, args):
        print("Processing single file")
        self._process_file(args.inputfile, args.outputfile, args)
        return True

    def process_folders(self, args):
        print("Processing folders")
        files = self._gather_files(args)
        for file in sorted(files):
            self._process_file(file[0], file[1], args)
        return True

    def _gather_files(self, args):
        files = []
        self._list_files(args.inputdir, args.outputdir, files)
        return files

    def _list_files(self, existing_base, new_base, files):
        for item in os.listdir(existing_base):
            if item[0] != ".":
                existing_full_path = os.path.join(existing_base, item)
                new_full_path = os.path.join(new_base, item)
                if os.path.isdir(existing_full_path):
                    new_full_path = os.path.join(new_base, item)
                    try:
                        os.makedirs(new_full_path)
                    except OSError as e:
                        pass
                    self._list_files(existing_full_path, new_full_path, files)
                else:
                    files.append((existing_full_path, new_full_path))

if __name__ == '__main__':

    processor = FileProcessor()
    parser = processor.create_base_args_parser()

    args = parser.parse_args()

    if processor.process(args) is False:
        parser.print_help()
        print("\n")
    