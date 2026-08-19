import fitz
from docx import Document


def load_pdf(file):

    text = ""

    pdf = fitz.open(
        stream=file.read(),
        filetype="pdf"
    )

    for page in pdf:
        text += page.get_text()

    pdf.close()

    return text


def load_docx(file):

    document = Document(file)

    text = ""

    for paragraph in document.paragraphs:

        if paragraph.text.strip():

            text += paragraph.text + "\n"

    return text


def load_txt(file):

    return file.read().decode(
        "utf-8",
        errors="ignore"
    )


def load_document(file):

    file_name = file.name.lower()

    if file_name.endswith(".pdf"):

        return load_pdf(file)

    elif file_name.endswith(".docx"):

        return load_docx(file)

    elif file_name.endswith(".txt"):

        return load_txt(file)

    else:

        raise ValueError(
            "Unsupported document format"
        )