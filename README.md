**Retrieval Augmented Generation (RAG) using Amazon Bedrock**
=====================================

A simple conversational AI chatbot built on top of Amazon Bedrock, enabling users to interact with their PDF file 

**Project Overview**
-------------------

This repository contains a Retrieval Augmented Generation (RAG) system using Amazon Bedrock, which allows users to
chat with their PDF files. The system uses Streamlit as the frontend framework and Docker for containerization.

**Features**

* Chat with your PDF files using a conversational interface
* Retrieve relevant information from PDFs in real-time
* Utilize Amazon Bedrock's retrieval-augmented generation capabilities

**How it Works**
----------------

The RAG system consists of three main components:

1. **Amazon Bedrock**: Provides the retrieval-augmented generation capabilities, enabling the system to retrieve
relevant information from PDFs.
2. **Streamlit**: Used as the frontend framework to create a user-friendly conversational interface for
interacting with the PDF files.
3. **Docker**: Containerizes the entire application, ensuring portability and ease of deployment.


**Technical Details**
--------------------

### Prerequisites

*   AWS Account
*   Amazon Bedrock setup
*   Python 3.12+ installed on your local machine
*   Streamlit 1.43 installed on your local machine

**Running the Chatbot**
----------------------

1.  Clone the repository: `git clone https://github.com/jcpunzalan123/chatbot_using_bedrock.git`
2.  Install dependencies: `pip install -r requirements.txt`
3.  Build the Docker image: `docker build -t your-image-name .`
4.  Run the container: `docker run -p 8083:8083 your-image-name`
5.  Access the application in your web browser: <http://localhost:8501>
