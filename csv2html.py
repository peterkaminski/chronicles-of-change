#!/usr/bin/env python3

# csv2html, a bespoke script for Chronicles of Change, to read the CSV data and write _books.html
#
# Usage: ./csv2html.py -i "site/Chronicles of Change_ Collapse, Resilience, and Humanity's Path Forward - Books.csv" -o templates/_books.html

import argparse
import csv
import html
import logging
import re

url_pattern = re.compile(r'https?://\S+')

def replace_urls_with_links(match):
    url = match.group(0)
    return f'<a href="{url}">{url}</a>'

def transform_row_to_html(row):
    """
    Transforms a CSV row into an HTML paragraph.

    Parameters:
        row (dict): A dictionary representing a row in the CSV file.

    Returns:
        str: A string containing the HTML paragraph.
    """
    try:
        title = html.escape(row['Title'])
        author = html.escape(row['Author(s)'])
        pub_date = html.escape(row['Publication Date'])
        url = html.escape(row['GoodReads URL'])
        desc = row['Description']

        # Replace URLs in the 'Description' field with HTML links
        desc = url_pattern.sub(replace_urls_with_links, desc)

        html_paragraph = f'<p><strong><a href="{url}">{title}</a></strong> by {author} (<strong>{pub_date}</strong>) {desc}</p>'
        return html_paragraph
    except KeyError as e:
        logging.error(f"Missing column in CSV: {e}")
        return ''

    except KeyError as e:
        logging.error(f"Missing column in CSV: {e}")
        return ''

    except KeyError as e:
        logging.error(f"Missing column in CSV: {e}")
        return ""
    except Exception as e:
        logging.error(f"Error while processing row: {e}")
        return ""

def read_csv_and_generate_html(input_file):
    """
    Reads a CSV file and generates HTML paragraphs.

    Parameters:
        input_file (str): The path to the input CSV file.

    Returns:
        str: A string containing the HTML content.
    """
    html_content = ""
    with open(input_file, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            html_content += transform_row_to_html(row) + "\n"
    return html_content

def main():
    parser = argparse.ArgumentParser(description="Transforms each row of a CSV file into an HTML paragraph.")
    parser.add_argument('-i', '--input', required=True, help="The input CSV file.")
    parser.add_argument('-o', '--output', required=True, help="The output HTML file.")

    args = parser.parse_args()

    input_file = args.input
    output_file = args.output

    try:
        html_content = read_csv_and_generate_html(input_file)

        with open(output_file, 'w') as html_file:
            html_file.write(html_content)

        print(f"HTML content has been written to {output_file}")

    except FileNotFoundError:
        logging.error(f"File {input_file} not found.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
