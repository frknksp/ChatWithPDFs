# Chat With Your PDFs

This project allows you to interact with your PDF files through a chat interface using OpenAI's GPT-3.5-turbo. Upload your PDFs, process them, and ask questions to retrieve information directly from the documents.

## Features

- Upload multiple PDF files.
- Process and store PDFs in a searchable database.
- Interact with your PDFs using natural language queries.
- Retrieve answers based on the content of your uploaded documents.


## Files

- **app.py**: The main application file that handles the Streamlit interface and interactions.
- **create_database.py**: Script to process and store PDF contents in a Chroma database.
- **query_data.py**: Script to query the database and interact with OpenAI's language model.

## Dependencies

- Streamlit
- langchain
- langchain_community
- langchain_openai
- Chroma
- dotenv

