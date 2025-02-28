import boto3
import streamlit as st
import os

## BEDROCK
from langchain_community.embeddings import BedrockEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader


## S3
s3_client = boto3.client("s3")
BUCKET_NAME = os.getenv("BUCKET_NAME")




def main():
    st.write("Chat with PDF using Amazon Bedrock!")
    upload_file = st.file_uploader("Choose a file", "pdf")


if __name__ == "__main__":
    main()