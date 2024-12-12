import os
import json
import openai
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

# Set up OpenAI API key
openai.api_key = 'your-openai-api-key'

# Initialize embeddings and vector database
embedding_model = OpenAIEmbeddings()
vector_db = Chroma(persist_directory='vector_db')

# Directory containing story files
story_dir = 'path/to/stories'

def compute_embeddings():
    for story_file in os.listdir(story_dir):
        if story_file.endswith('.txt'):
            with open(os.path.join(story_dir, story_file), 'r') as file:
                story_text = file.read()
            embeddings = embedding_model.embed(story_text)
            vector_db.add_document({'text': story_text, 'embeddings': embeddings})

    vector_db.persist()

if __name__ == '__main__':
    compute_embeddings()
