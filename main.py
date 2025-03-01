import boto3
import streamlit as st
import os
import uuid

## BEDROCK
from langchain_community.embeddings import BedrockEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader


## S3
s3_client = boto3.client("s3")
BUCKET_NAME = os.getenv("BUCKET_NAME")

def get_unique_id():
    return str(uuid.uuid4())


def main():
    st.write("Chat with PDF using Amazon Bedrock!")
    upload_file = st.file_uploader("Choose a file", "pdf")
    if upload_file is not None:
        request_id = get_unique_id()
        st.write(f"Request ID: {request_id}")
        saved_file_name = f"{request_id}.pdf"
        with open(saved_file_name, mode="wb") as w:
            w.write(upload_file.getvalue())

        loader = PyPDFLoader(saved_file_name)
        pages = loader.load_and_split()

        st.write(f"Total pages: {len(pages)}")


if __name__ == "__main__":
    main()