# Implement a Markdown => HTML converter
Reads a text file that uses Markdown formatting and writes converted html to a new file.

## Examples:
Sample Markdown:
```
Hello!

This is sample markdown for the [Mailchimp](https://www.mailchimp.com) homework assignment.
```
Output html:
```
<h1>Sample Document</h1>

<p>Hello!</p>

<p>This is sample markdown for the <a href="https://www.mailchimp.com">Mailchimp</a> homework assignment.</p>
```

## How to run:

```
python3 markdown_html_converter.py -markdownFile {path_to_markdown_file.txt} -htmlFile {filename_for_html_output}
```
to print the output to the console, run with <b> --p </b>

```
python3 markdown_html_converter.py -markdownFile {path_to_markdown_file.txt} --p
```

### Note:

If the output file doesn't exist, it will be created in the same directory as the markdown file.
If the filename <b> does exist </b> it will be overwritten.


If no output filename is provided, the output file will be written to `{markdown filename}_html.html`