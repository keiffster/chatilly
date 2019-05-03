import os
import re
import sys
import xml.etree.ElementTree as ET

def write_output_file(output_file, lines):

    with open(output_file, "w+") as xmlfile:

        xmlfile.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        xmlfile.write('<aiml>\n\n')

        for key in sorted(lines):
            for line in lines[key]:
                xmlfile.write(line)

        xmlfile.write('\n</aiml>\n')

def add_to_lines(lines, keys, pattern, pattern_text, pattern_key, that, template):
    
    if template is None:
        if that:
            line = "ERROR: <category>%s %s</category>\n"%(pattern, that)
        else:
            line = "ERROR: <category>%s</category>\n"%pattern
    else:
        if that:
            line = "<category>%s %s %s</category>\n"%(pattern, that, template)
        else:
            line = "<category>%s %s</category>\n"%(pattern, template)

    if pattern_key in keys:
        lines[pattern_key].append("DUPLICATE: %s"%line)
    else:
        keys.append(pattern_key)    
        lines[pattern_key] = [line]

def handle_pattern_match_formatting_issues(text):
    text = re.sub("\*", " * ", text)
    text = re.sub("_", " _ ", text)
    return text

def strip_spaces_whitespace(text):
    text = re.sub("\s+", " ", text)
    text = re.sub("\n", " ", text)
    text = re.sub(">\s*", ">", text)
    text = re.sub("\s*<", "<", text)
    return text

def extract_pattern_key(text):
    new_text = re.sub("\*|_", "", text)
    if new_text is None:
        return text
    return new_text.strip()

def extract_pattern(xmlcategory):
    for xmlpattern in xmlcategory.iter('pattern'):
        if xmlpattern.text is not None:
            pattern_text = xmlpattern.text.strip()
            pattern_text = pattern_text.upper()
            pattern_text = handle_pattern_match_formatting_issues(pattern_text)
            pattern_text = strip_spaces_whitespace(pattern_text)
            pattern_key = extract_pattern_key(pattern_text)
            pattern = "<pattern>%s</pattern>"%pattern_text.strip()
            return pattern, pattern_text, pattern_key
    return None, None, None

def extract_that(xmlcategory):
    for xmlthat in xmlcategory.iter("that"):
        that_text = ET.tostring(xmlthat)
        that = strip_spaces_whitespace(that_text)
        return that    
    return None

def strip_briefly(text):
    return re.sub(">.*[B|b]riefly,", ">", text)

def replace_means(text):
    return re.sub("means", "<srai>DEFINITION MEANS</srai> ", text)

def add_sentence_start(text):
    return re.sub("<template>", "<template> <srai>DEFINITION START</srai> ", text)

def remove_emotion(text):
    return re.sub('<think><set name="emotion">.*</set></think>', "", text)

def replace_yes(text):
    return re.sub("Yes.", "<srai>DEFINITION YES</srai> ", text)

def extract_template(xmlcategory, options):
    for xmltemplate in xmlcategory.iter("template"):
        template_text = ET.tostring(xmltemplate)
        template = strip_spaces_whitespace(template_text)
        if options.briefly:
            template = strip_briefly(template)
        if options.means:
            template = replace_means(template)
        if options.emotion:
            template = remove_emotion(template)
        if options.sentence:
            template = add_sentence_start(template)
        if options.yes:
            template = replace_yes(template)
        return template   
    return None

def parse_categories(aiml, options):
    lines = {}
    keys = []
    for xmlcategory in aiml.findall('category'):

        pattern, pattern_text, pattern_key = extract_pattern(xmlcategory)

        if pattern is not None:
            that = extract_that(xmlcategory)

            template = extract_template(xmlcategory, options)

            add_to_lines(lines, keys, pattern, pattern_text, pattern_key, that, template)

    return lines

def convert_file (input_file, output_file, options):
    tree = ET.parse(input_file)
    aiml = tree.getroot()

    lines = parse_categories(aiml, options)

    if options.dummy is False:
       write_output_file(output_file, lines)

def convert_folders(existing_base, new_base, options):
    files = []
    list_files(existing_base, new_base, files)
    for file in sorted(files):
        print(file[0])
        convert_file(file[0], file[1], options)

def list_files(existing_base, new_base, files):
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
                list_files(existing_full_path, new_full_path, files)
            else:
                files.append((existing_full_path, new_full_path))

if __name__ == '__main__':

    exit(0)
    import argparse

    parser = argparse.ArgumentParser(description='AIML Utilities')
    
    parser.add_argument('-if', '--inputfile', action="store", dest="inputfile", help="Input file")
    parser.add_argument('-of', '--outputfile', action="store", dest="outputfile", help="Output file")
    parser.add_argument('-id', '--inputdir', action="store", dest="inputdir", help="Input dir")
    parser.add_argument('-od', '--outputdir', action="store", dest="outputdir", help="Output dir")

    parser.add_argument('-briefly', action="store", dest="briefly", default=False, help="Add briefly SRAI")
    parser.add_argument('-means', action="store", dest="means", default=False, help="Add means SRAI")
    parser.add_argument('-emotion', action="store", dest="means", default=False, help="Add emotion SRAI")
    parser.add_argument('-sentence', action="store", dest="means", default=False, help="Add sentece start SRAI")
    parser.add_argument('-yes', action="store", dest="means", default=False, help="Add yes SRAI")

    parser.add_argument('-verbose', action="store", dest="verbose", default=False, help="Verbose output")
    parser.add_argument('-dummy', action="store", dest="dummy", default=False, help="Don't modify output file(s)")

    args = parser.parse_args()

    if args.inputfile and args.outputfile:
        convert_folders(args.inputfile, args.outputfile, args)
    elif args.inputdir and args.outputdir:
        convert_dir(args.inputdir, args.outputdir, args)
    else:
        parser.print_help()
    