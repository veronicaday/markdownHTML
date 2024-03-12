import argparse
import sys
import os


#https://stackoverflow.com/questions/14360389/getting-file-path-from-command-line-argument-in-python
def create_arg_parser():
    # Creates and returns the ArgumentParser object
    parser = argparse.ArgumentParser(description='Convert a markdown text file into an html file')
    parser.add_argument('markdownFile', help='Path to the markdown text file.')
    parser.add_argument('--htmlFile', help='Path to where to store the output html file.')
    return parser


# Generator for reading the next line of the file. Does not pull entire file into memory
def read_next_line(markdown_filename: str):
    with open(markdown_filename) as file:
        while line := file.readline():
            yield line


def convert_markdown_header(line: str) -> str:
    i = 0
    count_header = 0
    while i < len(line) and line[i] == '#' and count_header <= 7:
        i += 1
        count_header += 1

    if count_header >= 7:
        return convert_markdown_paragraph(line)
    if line[i] != ' ':
        return convert_markdown_paragraph(line)

    header_open = f'<h{count_header}>'
    header_close = f'/<h{count_header}>'
    return f"{header_open}{line[i+1:]}{header_close}"


def convert_markdown_paragraph(line: str) -> str:
    return f"<p>{line}</p>"


def convert_markdown_hyperlinks(line: str) -> str:
    return line

# Accepts a string of markdown and returns a string of HTML
def convert_markdown_line(line: str) -> str:
    if not line:
        return ""

    if line[0] == '#':
        line = convert_markdown_header(line)
    else:
        line = convert_markdown_paragraph(line)
    return line
    # i = 0
    # while i < len(line):
    #     if char == '[':
    #         link_start = i
    #         link_end = i+1
    #         while link_end < len(line) and line[link_end] != ']':
    #             link_end += 1
    #         if link_end and link_end+1 < len(line) and line[link_end+1] == '(':
    #             url_start = link_end+1
    #             url_end = link_end+2
    #             while url_end < len(line) and line[url_end] != ')':
    #                 if url_end == ' ':
    #                     break
    #                 url_end += 1
    #         else:
    #             continue
    #         if url_end < len(line):
    #             link_text = line[link_start:link_end+1]
    #             url_text = line[url_start:url_end + 1]
    #             line = line[:url_end] + convert_markdown_hyperlink(link_text, url_text) + line[url_end+1:]
    #             i = url_end + 1
    #     i += 1







# Writes string to html file
def write_to_html_file(line: str, output_filename: str):
    # if output file does not exist, create it
    # open file and write line; close file
    print(line)


def convert_markdown_file(markdown_filename: str, output_filename: str):
    for line in read_next_line(markdown_filename):
        converted = convert_markdown_line(line.rstrip())
        write_to_html_file(converted, output_filename)


if __name__ == '__main__':
    arg_parser = create_arg_parser()
    parsed_args = arg_parser.parse_args(sys.argv[1:])
    if not os.path.exists(parsed_args.markdownFile):
        print("Error: markdown file not found")

    # TODO: create new file if not provided
    output_file = parsed_args.htmlFile
    convert_markdown_file(parsed_args.markdownFile, parsed_args.htmlFile)
    print(f"Successfully converted {parsed_args.markdownFile} to html: {parsed_args.htmlFile}")

