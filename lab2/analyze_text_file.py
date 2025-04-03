import re
from collections import Counter
import os

TEST_FILE_PATH = os.path.join("test_file.md")


def analyze_text_file(filename: str) -> dict:
    try:
        with open(filename, "r", encoding="utf-8") as file:
            content = file.read()
    except Exception as e:
        print("Shit")
        return {"error": f"Could not read file: {str(e)}"}

    # Common English stop words to filter out from frequency analysis
    stop_words = {
        "the",
        "a",
        "an",
        "and",
        "or",
        "but",
        "in",
        "on",
        "at",
        "to",
        "for",
        "with",
        "by",
        "about",
        "as",
        "into",
        "like",
        "through",
        "after",
        "over",
        "between",
        "out",
        "of",
        "is",
        "are",
        "was",
        "were",
        "be",
        "been",
        "being",
        "have",
        "has",
        "had",
        "do",
        "does",
        "did",
        "this",
        "that",
        "these",
        "those",
        "it",
        "its",
        "from",
        "there",
        "their",
    }

    def count_words(word_regex,words_content):
        return len(re.findall(word_regex,words_content))

    # Implement word extraction using regex
    # Find all words in the content (lowercase for consistency)
    word_regex = r'(?P<word>([A-Z]|[a-z])[a-z]*)(\s|\,|\.|\!|\?)'
    words = [ word.group("word").lower() for word in re.finditer(word_regex,content) ]
    word_count = len(words)

    # Implement sentence splitting using regex
    # A sentence typically ends with ., !, or ? followed by a space
    # Be careful about abbreviations (e.g., "Dr.", "U.S.A.")
    sentence_pattern = r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s'
    sentences = [ element for element in re.finditer(sentence_pattern, content) ]
    sentence_count = len([s for s in sentences if str(s).strip()])

    # Implement email extraction using regex
    # Extract all valid email addresses from the content
    email_pattern = r"([A-Za-z\-]+\.)*[A-Za-z\-]+@([A-Za-z\-]+\.)+[A-Za-z\-]+"
    emails = [ email.group() for email in re.finditer(email_pattern,content) ]

    # Calculate word frequencies
    # Count occurrences of each word, excluding stop words and short words
    # Use the Counter class from collections
    filtered_words = [word for word in words if word not in stop_words]
    word_counter = Counter(filtered_words)
    most_frequent_words = {word: count for word, count in word_counter.most_common() if count > 1}


    # Implement date extraction with multiple formats
    # Detect dates in various formats: YYYY-MM-DD, DD.MM.YYYY, MM/DD/YYYY, etc.
    # Create multiple regex patterns for different date formats
    date_patterns = [
    r"(\d{4})-(0[1-9]|1[0-2])-([0-2][0-9]|3[0-1])",  # YYYY-MM-DD
    r"([0-2][0-9]|3[0-1])-(0[1-9]|1[0-2])-(\d{4})",  # DD-MM-YYYY
    r"(0[1-9]|1[0-2])-([0-2][0-9]|3[0-1])-(\d{4})",  # MM-DD-YYYY
    r"([0-2][0-9]|3[0-1])\.(0[1-9]|1[0-2])\.(\d{4})",  # DD.MM.YYYY
    r"(0[1-9]|1[0-2])\/([0-2][0-9]|3[0-1])\/(\d{4})",  # MM/DD/YYYY
    r"(\d{4})\/(0[1-9]|1[0-2])\/([0-2][0-9]|3[0-1])",  # YYYY/MM/DD
    r"(\d{4})\.(0[1-9]|1[0-2])\.([0-2][0-9]|3[0-1])",  # YYYY.MM.DD
    r"(January|February|March|April|May|June|July|August|September|October|November|December) ([0-2][0-9]|3[0-1]), (\d{4})",  # Month DD, YYYY
    r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) ([0-2][0-9]|3[0-1]), (\d{4})"  # MMM DD, YYYY
    ]
    dates = []
    for pattern in date_patterns:
        dates = dates + [ date.group() for date in re.finditer(pattern, content) ]

    # Analyze paragraphs
    # Split the content into paragraphs and count words in each
    # Paragraphs are typically separated by one or more blank lines
    # paragraphs = re.split(r".{10,}\n+", content)
    
    paragraphs = re.finditer(r'.+\n+', content)
    paragraph_sizes = { i:count_words(word_regex,paragraph.group()) for i,paragraph in enumerate(paragraphs) }
    paragraph_sizes = { key: value for key, value in paragraph_sizes.items() if 0 != value }
    result = {
        "word_count": word_count,
        "sentence_count": sentence_count,
        "emails": emails,
        "frequent_words": most_frequent_words,
        "dates": dates,
        "paragraph_sizes": paragraph_sizes,
    }
    print(result)
    return result
 
def main():
    analyze_text_file(TEST_FILE_PATH)

if __name__ == "__main__":
    main()
