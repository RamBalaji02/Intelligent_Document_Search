import re


# Stop words
STOP_WORDS = {
    "a", "an", "the", "and", "or", "but",
    "if", "then", "else", "for", "of",
    "to", "in", "on", "at", "by", "with",
    "from", "as", "is", "are", "was",
    "were", "be", "been", "being",
    "this", "that", "these", "those",
    "it", "its", "he", "she", "they",
    "them", "we", "you", "your",
    "i", "me", "my", "our", "ours",
    "their", "theirs", "his", "her",
    "has", "have", "had", "do", "does",
    "did", "can", "could", "will",
    "would", "should", "may", "might",
    "not", "no", "so", "than",
    "too", "very", "also"
}


def preprocess_text(text):

    # 1. Convert text to lowercase
    lowercase_text = text.lower()

    # 2. Remove punctuation
    text_without_punctuation = re.sub(
        r"[^\w\s]",
        "",
        lowercase_text
    )

    # 3. Tokenization
    tokens = text_without_punctuation.split()

    # 4. Remove stop words
    processed_tokens = []

    for word in tokens:

        if word not in STOP_WORDS:
            processed_tokens.append(word)

    # 5. Convert tokens back into text
    processed_text = " ".join(
        processed_tokens
    )

    # Return all results
    return {
        "lowercase_text": lowercase_text,
        "without_punctuation": text_without_punctuation,
        "tokens": tokens,
        "processed_tokens": processed_tokens,
        "processed_text": processed_text
    }