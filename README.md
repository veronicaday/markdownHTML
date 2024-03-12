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
python3 markdown_html_converter.py {path_to_markdown_file.txt} {path_to_write_html_output}
```