import re
from typing import Optional

def parse_publication(reference: str) -> Optional[dict]:
    """
    Parse academic publication reference and extract structured information.

    Expected reference format:
    Lastname, I., Lastname2, I2. (Year). Title. Journal, Volume(Issue), StartPage-EndPage.

    Example:
    Kowalski, J., Nowak, A. (2023). Analiza algorytmów tekstowych. Journal of Computer Science, 45(2), 123-145.

    Args:
        reference (str): Publication reference string

    Returns:
        Optional[dict]: A dictionary containing parsed publication data or None if the reference doesn't match expected format
    """
    # Implement regex patterns to match different parts of the reference
    # You need to create patterns for:
    # 1. Authors and year pattern
    # 2. Title and journal pattern
    # 3. Volume, issue, and pages pattern
    authors_year_pattern = r"(?P<authors>(([A-ZŻŹĆĄŚĘŁÓŃ][a-zżźćńółąśę]+\s*,\s*[A-ZŻŹĆĄŚĘŁÓŃ]\.\s*),{0,1}\s*)+)\((?P<year>\d{4})\)"
    title_journal_pattern = r"\.\s*(?P<title>.+?)\.\s*(?P<journal>.+?),"
    volume_issue_pages_pattern = r"\s*(?P<volume>\d+)(?:\((?P<issue>\d+)\))?,\s*(?P<start_page>\d+)-(?P<end_page>\d+)\."

    # Combine the patterns
    full_pattern = authors_year_pattern + title_journal_pattern + volume_issue_pages_pattern
    # Use re.match to try to match the full pattern against the reference
    # If there's no match, return None
    matches = re.match(full_pattern, reference)

    # Extract information using regex
    # Each author should be parsed into a dictionary with 'last_name' and 'initial' keys
    if not matches:
        return None 
    
    authors_text = matches.group("authors")
    
    # Create a pattern to match individual authors
    author_pattern = r"(?P<last_name>[A-ZŻŹĆĄŚĘŁÓŃ][a-zżźćńółąśę]+),\s*(?P<initial>[A-ZŻŹĆĄŚĘŁÓŃ])\.,{0,1}\s"
    # Use re.finditer() to extract all authors in the correct order
    authors_list = []
    for author in re.finditer(author_pattern, authors_text):
        authors_list.append({"last_name": author.group('last_name'), "initial": author.group('initial')})
    # Create and return the final result dictionary with all the parsed information
    # It should include authors, year, title, journal, volume, issue, and pages

    result = {
        "authors": authors_list,
        "year": int(matches.group("year")),
        "title": matches.group("title"),
        "journal": matches.group("journal"),
        "volume": int(matches.group("volume")),
        "issue": int(matches.group("issue")) if matches.group("issue") else None,
        "pages": {
            "start": int(matches.group("start_page")),
            "end": int(matches.group("end_page")),
        },
    }

    return result

