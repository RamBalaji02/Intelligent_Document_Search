from sentence_transformers import SentenceTransformer


# Load embedding model

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def generate_embedding(text):

    embedding = model.encode(
        text,
        convert_to_numpy=True
    )

    return embedding


def generate_document_embeddings(
    documents
):

    results = []


    for document in documents:

        embedding = generate_embedding(
            document["text"]
        )


        results.append({

            "name":
                document["name"],

            "text":
                document["text"],

            "embedding":
                embedding

        })


    return results