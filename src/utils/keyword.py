import re
import spacy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load spaCy model
nlp = spacy.load('en_core_web_sm')

# Define phrases to search for and variations
keywords = [
    r'\b(don\'t|do not|do n\'t) (remove|take off|clear) (hard )?hold\b',
    r'\bpermanent hold\b',
    # Add more patterns here
]

# Sample data
comments = [
    "Do not remove hard hold",
    "Please don’t take off the hold",
    "Permanent hold placed on account",
    # Add more comment examples
]

# Search using regex and NLP similarity
def search_comments(comments, keywords):
    matches = []
    for comment in comments:
        for keyword in keywords:
            if re.search(keyword, comment, re.IGNORECASE):
                matches.append((comment, "regex match"))
                break
        else:
            # NLP matching for broader similarity
            comment_doc = nlp(comment)
            for phrase in ["Do not remove hard hold", "permanent hold"]:
                phrase_doc = nlp(phrase)
                if comment_doc.similarity(phrase_doc) > 0.75:  # Threshold for similarity
                    matches.append((comment, "NLP similarity match"))
                    break
    return matches

# Run search
results = search_comments(comments, keywords)
for result in results:
    print(result)
