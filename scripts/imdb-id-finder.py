#!/usr/bin/env python3
"""
Script to extract IMDb IDs from a list of movie titles with years.
Usage: python imdb_id_finder.py [input_file]
If no input file is provided, reads from stdin.
"""

import re
import fileinput
import requests
import urllib.parse

# Match pattern: Title (Year) rest of text
regex_movieyear = r"(.*?)\s*\((\d{4})\).*"

def parse_movie_entry(line):
    """Extract title and year from a movie entry line."""
    match = re.match(regex_movieyear, line)
    if match:
        title = match.group(1).strip()
        year = match.group(2)
        return title, year
    return None, None


def search_imdb_id(title, year):
    """Search for IMDb ID using OMDb API."""
    # Note: In a production environment, you should use your own API key
    # You can get a free key at https://www.omdbapi.com/apikey.aspx
    api_key = "277555d2"  # Replace with your actual API key
    
    args = urllib.parse.urlencode(dict(t=title, y=year, apikey=api_key))
    try:
        response = requests.get(f"http://www.omdbapi.com/?{args}")
        data = response.json()
        
        if data.get("Response") == "True" and "imdbID" in data:
            return {
                "title": title,
                "year": year,
                "imdb_id": data["imdbID"],
                "found_title": data.get("Title", ""),
                "found_year": data.get("Year", "")
            }
        return {
            "title": title,
            "year": year,
            "imdb_id": None,
            "error": data.get("Error", "Unknown error")
        }
    except Exception as e:
        return {
            "title": title,
            "year": year,
            "imdb_id": None,
            "error": str(e)
        }

def main():
    for line in fileinput.input():
        if '# ' in line:
            precomment, comment = line.split('# ')
            comment = ' # ' + comment
        else:
            precomment, comment = line, ''
        precomment = precomment.strip()
        if not precomment:
            print(line)
            continue

        match = re.match(regex_movieyear, precomment)
        if not match:
            print(f'# {precomment}')
            continue

        title = match.group(1).strip()
        year = match.group(2)

        result = search_imdb_id(title, year)
        if not result["imdb_id"]:
            print(f"# NOT FOUND: {result['title']} ({result['year']}){comment}")
        else:
            print(f"{result['imdb_id']} # {result['found_title']} ({result['year']}){comment}")

if __name__ == "__main__":
    main()
