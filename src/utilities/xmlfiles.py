import os
import re
import sys
import xml.etree.ElementTree as ET

from files import FileProcessor


class XMLFileProcessor(FileProcessor):

    @staticmethod
    def get_title():
        return 'AIML XML File Processor'

    def _process_element(self, element, args):
        if args.verbose:
            print("\t[%s]"%ET.tostring(element))
        return None

    def _process_file(self, inputfilename, outputfilename, args):
        print("Converting [%s] -> [%s]"%(inputfilename, outputfilename))

        tree = ET.parse(inputfilename)
        aiml = tree.getroot()

        elements = []
        for xmlelement in aiml.iter('pattern'):
            new_element = self._process_element(xmlelement, args)
            if new_element:
                elements.append(new_element)


if __name__ == '__main__':

    processor = XMLFileProcessor()
    parser = processor.create_base_args_parser()

    args = parser.parse_args()

    if processor.process(args) is False:
        parser.print_help()
        print("\n")
    