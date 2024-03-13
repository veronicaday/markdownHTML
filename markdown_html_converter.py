import argparse
import sys
import os
from typing import Optional


#https://stackoverflow.com/questions/14360389/getting-file-path-from-command-line-argument-in-python
def create_arg_parser():
    # Creates and returns the ArgumentParser object
    parser = argparse.ArgumentParser(description='Convert a markdown text file into an html file')
    parser.add_argument('-markdownFile', dest='markdown_file', required=True, help='Path to the markdown text file.')
    parser.add_argument('-htmlFile', dest="html_file", required=False, help='Path to where to store the output html file.')
    parser.add_argument('--p', dest="print_opt", action="store_true", required=False, help='Include to print line by line output to console.')
    return parser


# Generator for reading the next line of the file.
# Does not pull entire file into memory, but reads line by line
def read_next_line(markdown_filename: str):
    with open(markdown_filename, encoding="utf-8") as file:
        while line := file.readline():
            yield line


# Returns the line including the proper header tags
def convert_markdown_header(line: str) -> str:
    i = 0
    count_header = 0
    while i < len(line) and line[i] == '#' and count_header <= 7:
        i += 1
        count_header += 1

    # cannot have <h7> or higher
    if count_header >= 7:
        return convert_markdown_paragraph(line)
    if line[i] != ' ':
        return convert_markdown_paragraph(line)

    header_open = f'<h{count_header}>'
    header_close = f'</h{count_header}>'
    return f"{header_open}{line[i+1:]}{header_close}"


# Returns the line including paragraph tags
def convert_markdown_paragraph(line: str) -> str:
    return f"<p>{line}</p>"


# Returns the line including <a> tags with the href set
def convert_markdown_hyperlink(link_text: str, url_hyperlink: str) -> str:
    return f'<a href="{url_hyperlink}">{link_text}</a>'


# Looks for any hyperlinks and adds appropriate html tags if found
def convert_markdown_hyperlinks(line: str) -> str:
    def find_link_text_end(link_start: int) -> int:
        link_end = link_start
        while link_end < len(line) and line[link_end] != ']':
            link_end += 1
        return link_end

    def find_url_end(url_start: int) -> int:
        url_end = url_start
        while url_end < len(line) and line[url_end] != ')':
            if url_end == ' ':
                return len(line)
            url_end += 1
        return url_end

    i = 0
    while i < len(line):
        if line[i] == '[':
            link_start = i+1
            link_end = find_link_text_end(link_start)

            if link_end and link_end + 1 < len(line) and line[link_end + 1] == '(':
                url_start = link_end + 2
                url_end = find_url_end(url_start)
            else:
                i+=1
                continue
            if url_end < len(line):
                link_text = line[link_start:link_end]
                url_text = line[url_start:url_end]
                line = line[:i] + convert_markdown_hyperlink(link_text, url_text) + line[url_end+1:]
                i = url_end
        i += 1
    return line


# Accepts a string of markdown and returns a string of HTML
def convert_markdown_line(line: str) -> str:
    if not line:
        return ""

    if line[0] == '#':
        line = convert_markdown_header(line)
    else:
        line = convert_markdown_paragraph(line)
    return convert_markdown_hyperlinks(line)


# Writes string to html file
# If this is the first time we are writing to the file, assume we want to overwrite existing content
# otherwise we want to append
def write_to_html_file(line: str, output_filename: str, first_write: bool = False):
    mode = 'w+' if first_write else 'a+'
    with open(output_filename, mode, encoding="utf-8") as file:
        file.write(line)


# Converts the Markdown File to HTML File
# If error occurs, will print to console and attempt to continue writing subsequent lines
def convert_markdown_file(markdown_filename: str, output_filename: str, print_output: bool = False):
    # create if file does not exist, otherwise wipe current file contents
    write_to_html_file('', output_filename, first_write=True)
    for line in read_next_line(markdown_filename):
        try:
            converted = convert_markdown_line(line.rstrip())
        except Exception as e:
            print(f"ERROR: Could not convert markdown line: {line}", e)
            continue

        try:
            write_to_html_file(f"{converted}\n", output_filename)
            if print_output:
                print(converted)
        except Exception as e:
            print(f"ERROR: Could not write to file html line: {converted}", e)
            continue


def create_html_filename(input_file_path: str, output_filename: Optional[str]) -> str:
    def get_filename_from_path(path: str) -> str:
        base_name = os.path.basename(input_file_path)
        return os.path.splitext(base_name)[0]


    output_filename = output_filename or f"{get_filename_from_path(input_file_path)}_html.html"
    directory_path = os.path.dirname(input_file_path)
    return os.path.join(directory_path, output_filename)


if __name__ == '__main__':
    arg_parser = create_arg_parser()
    parsed_args = arg_parser.parse_args(sys.argv[1:])
    if not os.path.exists(parsed_args.markdown_file):
        print("ERROR: markdown file not found.")
        sys.exit()

    input_file = parsed_args.markdown_file
    output_file = create_html_filename(input_file, parsed_args.html_file)
    convert_markdown_file(input_file, output_file, parsed_args.print_opt)
    print(f"SUCCESS: Converted {parsed_args.markdown_file} to: {output_file}")

