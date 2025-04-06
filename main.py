import boto3
import botocore.config

import streamlit as st
import json
import os
import uuid

## BEDROCK
from langchain_community.embeddings import BedrockEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

from langchain_community.vectorstores import FAISS

## S3
s3_client = boto3.client("s3")
BUCKET_NAME = os.getenv("BUCKET_NAME")

bedrock_client = boto3.client(service_name="bedrock-runtime", region_name="us-east-1",
                             config=botocore.config.Config(read_timeout=300, retries={'max_attempts': 3}))
bedrock_embeddings = BedrockEmbeddings(model_id="us.meta.llama3-1-8b-instruct-v1:0", client=bedrock_client)


def get_unique_id():
    return str(uuid.uuid4())


def call_bedrock_model(body):
    try:
        bedrock=boto3.client(service_name="bedrock-runtime", region_name="us-east-1",
                             config=botocore.config.Config(read_timeout=300, retries={'max_attempts': 3}))
        bedrock.invoke_model(body=json.dumps(body), modelId="meta.llama3-1-8b-instruct-v1:0")
    except Exception as e:
        print(f"Error: {e}")


# def analyze_pdf_using_bedrock(pdf_file):
#     prompt=f"""<s>[INST] Human: Analyze and summarize the context of {pdf_file} by writing 4-5 sentences
#     Assitant: [/INST]
#     """

#     body = {
#         "prompt": prompt,
#         "max_gen_len": 512,
#         "temperature": 0.5,
#         "top_p": 0.9
#     }

#     call_bedrock_model(body)


def lambda_handler(event, context):
    return{
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }


def split_text(pages, chunk_size, chunk_overlap):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    docs = text_splitter.split_documents(pages)
    return docs


def create_vector_store(request_id, documents):
    vectorstore_faiss = FAISS.from_documents(documents, bedrock_embeddings)
    file_name = f"{request_id}.bin"
    folder_path = "/tmp/"
    vectorstore_faiss.save_local(index_name=file_name, folder_path=folder_path)

    #upload to s3 bucket
    s3_client.upload(Filename= folder_path + "/" + file_name + ".faiss", Bucket=BUCKET_NAME, key="my_faiss.faiss")
    s3_client.upload(Filename= folder_path + "/" + file_name + ".pkl", Bucket=BUCKET_NAME, key="my_faiss.pkl")
    return True


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

        # Split Text
        splitted_docs = split_text(pages, 1000, 200)
        st.write(f"Splitted Docs length: {len(splitted_docs)}")
        st.write("================")
        st.write(splitted_docs[0])
        st.write("================")
        st.write(splitted_docs[1])

        result = create_vector_store(request_id, splitted_docs)
        if result:
            st.write("PDF processed sucessfully.")
        else:
            st.write("Error. Please check logs.")

if __name__ == "__main__":
    main()