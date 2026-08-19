from sklearn.metrics.pairwise import cosine_similarity

from src.embeddings import generate_embedding


def semantic_search(
    query,
    document_embeddings,
    top_k=3
):

    if not query.strip():

        return []


    # Convert query into embedding

    query_embedding = generate_embedding(
        query
    )


    results = []


    for document in document_embeddings:

        document_embedding = (
            document["embedding"]
        )


        similarity = cosine_similarity(

            [query_embedding],

            [document_embedding]

        )[0][0]


        results.append({

            "name":
                document["name"],

            "text":
                document["text"],

            "similarity":
                float(similarity)

        })


    # Highest similarity first

    results.sort(
        key=lambda item:
        item["similarity"],
        reverse=True
    )


    # Top 3

    return results[:top_k]