import re


def search_keyword(documents, keyword):

    results = []

    keyword = keyword.strip().lower()

    if not keyword:

        return results


    for document in documents:

        name = document["name"]

        text = document["text"]

        lower_text = text.lower()


        # Count occurrences

        pattern = (
            r"\b"
            + re.escape(keyword)
            + r"\b"
        )

        occurrences = len(
            re.findall(
                pattern,
                lower_text
            )
        )


        # Find matching sentences

        sentences = re.split(
            r"[.!?]+",
            text
        )


        matching_sentences = []

        for sentence in sentences:

            if keyword in sentence.lower():

                sentence = sentence.strip()

                if sentence:

                    matching_sentences.append(
                        sentence
                    )


        if occurrences > 0:

            results.append({

                "name": name,

                "occurrences":
                    occurrences,

                "sentences":
                    matching_sentences
            })


    # Highest occurrence first

    results.sort(
        key=lambda item:
        item["occurrences"],
        reverse=True
    )


    return results