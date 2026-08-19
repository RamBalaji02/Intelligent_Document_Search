import streamlit as st
import re

from src.document_loader import load_document
from src.preprocessing import preprocess_text
from src.keyword_search import search_keyword
from src.embeddings import generate_document_embeddings
from src.semantic_search import semantic_search


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(

    page_title=
        "Intelligent Document Search",

    page_icon="🔎",

    layout="wide"
)


# ==================================================
# TITLE
# ==================================================

st.title(
    "🔎 Intelligent Document Search"
)

st.write(
    "An NLP-based document search system "
    "using keyword search, semantic search "
    "and LLM-based question answering."
)


# ==================================================
# FILE UPLOAD
# ==================================================

uploaded_files = st.file_uploader(

    "Upload Documents",

    type=[
        "pdf",
        "docx",
        "txt"
    ],

    accept_multiple_files=True
)


# ==================================================
# LOAD DOCUMENTS
# ==================================================

documents = []


if uploaded_files:

    for file in uploaded_files:

        try:

            text = load_document(
                file
            )


            documents.append({

                "name":
                    file.name,

                "text":
                    text

            })


        except Exception as error:

            st.error(
                f"Could not read "
                f"{file.name}: {error}"
            )


# ==================================================
# DOCUMENT PROCESSING
# ==================================================

if documents:

    st.header(
        "📄 Part 1 — Document Processing"
    )


    for document in documents:

        text = document["text"]


        word_count = len(
            text.split()
        )


        sentences = re.split(
            r"[.!?]+",
            text
        )


        sentences = [

            sentence.strip()

            for sentence in sentences

            if sentence.strip()

        ]


        st.markdown("---")


        st.subheader(
            f"📄 {document['name']}"
        )


        col1, col2 = st.columns(2)


        with col1:

            st.metric(
                "Number of Words",
                word_count
            )


        with col2:

            st.metric(
                "Number of Sentences",
                len(sentences)
            )


        with st.expander(
            "View Extracted Text"
        ):

            st.text_area(

                "Document Content",

                text,

                height=250,

                key=
                    f"text_{document['name']}"

            )


# ==================================================
# NLP PREPROCESSING
# ==================================================

if documents:

    st.header(
        "🧠 Part 2 — NLP Text Preprocessing"
    )

    # Select document
    selected_document = st.selectbox(
        "Select a document",
        [
            document["name"]
            for document in documents
        ],
        key="preprocessing_document"
    )

    # Get selected document text
    selected_text = ""

    for document in documents:

        if document["name"] == selected_document:

            selected_text = document["text"]

            break

    # Process text
    processed = preprocess_text(
        selected_text
    )


    # ------------------------------------------
    # 1. Original Text
    # ------------------------------------------

    st.subheader(
        "1. Original Text"
    )

    st.text_area(
        "Original document text",
        selected_text,
        height=200,
        key="original_document_text"
    )


    # ------------------------------------------
    # 2. Lowercase
    # ------------------------------------------

    st.subheader(
        "2. Lowercase"
    )

    st.text_area(
        "Lowercase text",
        processed["lowercase_text"],
        height=150,
        key="lowercase_output"
    )


    # ------------------------------------------
    # 3. Remove Punctuation
    # ------------------------------------------

    st.subheader(
        "3. Remove Punctuation"
    )

    st.text_area(
        "Text without punctuation",
        processed["without_punctuation"],
        height=150,
        key="punctuation_output"
    )


    # ------------------------------------------
    # 4. Tokenization
    # ------------------------------------------

    st.subheader(
        "4. Tokenization"
    )

    tokens = processed["tokens"]

    st.write(
        f"Total Tokens: **{len(tokens)}**"
    )

    st.text_area(
        "Tokenized Words",
        " | ".join(tokens),
        height=250,
        key="tokenization_output"
    )


    # ------------------------------------------
    # 5. Remove Stop Words
    # ------------------------------------------

    st.subheader(
        "5. Remove Stop Words"
    )

    processed_tokens = (
        processed["processed_tokens"]
    )

    st.write(
        "Total Tokens After Stop Word Removal: "
        f"**{len(processed_tokens)}**"
    )

    st.text_area(
        "Words after removing stop words",
        " | ".join(processed_tokens),
        height=250,
        key="stopword_output"
    )


    # ------------------------------------------
    # 6. Final Preprocessed Text
    # ------------------------------------------

    st.subheader(
        "6. Final Preprocessed Text"
    )

    st.text_area(
        "Final processed text",
        processed["processed_text"],
        height=250,
        key="final_preprocessed_output"
    )


# ==================================================
# KEYWORD SEARCH
# ==================================================

if documents:

    st.header(
        "🔍 Part 3 — Keyword-Based Search"
    )


    keyword = st.text_input(

        "Enter Keyword",

        placeholder=
            "Example: artificial intelligence"

    )


    if st.button(
        "Search Keyword"
    ):

        if not keyword.strip():

            st.warning(
                "Please enter a keyword."
            )

        else:

            results = search_keyword(

                documents,

                keyword

            )


            if results:

                st.success(

                    f"{len(results)} "
                    f"matching document(s) found."

                )


                for result in results:

                    st.markdown("---")


                    st.subheader(

                        f"📄 {result['name']}"

                    )


                    st.metric(

                        "Keyword Occurrences",

                        result[
                            "occurrences"
                        ]

                    )


                    if result[
                        "sentences"
                    ]:

                        st.write(
                            "### Matching Sentences"
                        )


                        for sentence in result[
                            "sentences"
                        ]:

                            st.info(
                                sentence
                            )


            else:

                st.warning(

                    f"No documents found "
                    f"for '{keyword}'."

                )


# ==================================================
# SEMANTIC SEARCH
# ==================================================

if documents:

    st.header(
        "🧠 Part 4 — Semantic Search"
    )


    semantic_query = st.text_input(

        "Enter a semantic search query",

        placeholder=
            "Example: How do computers learn from data?"

    )


    if st.button(
        "Search Semantically"
    ):

        if not semantic_query.strip():

            st.warning(
                "Please enter a query."
            )

        else:

            with st.spinner(
                "Generating embeddings..."
            ):

                document_embeddings = (
                    generate_document_embeddings(
                        documents
                    )
                )


            results = semantic_search(

                semantic_query,

                document_embeddings,

                top_k=3

            )


            if results:

                st.success(
                    "Top 3 relevant documents"
                    " found."
                )


                for index, result in enumerate(

                    results,

                    start=1

                ):

                    similarity = (
                        result["similarity"]
                        * 100
                    )


                    st.markdown("---")


                    st.subheader(

                        f"{index}. "
                        f"📄 {result['name']}"

                    )


                    st.metric(

                        "Similarity",

                        f"{similarity:.2f}%"

                    )


                    with st.expander(
                        "View Document"
                    ):

                        st.write(
                            result["text"]
                        )


            else:

                st.warning(
                    "No relevant documents found."
                )

