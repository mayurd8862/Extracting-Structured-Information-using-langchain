import os
import chromadb
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from chromadb.config import Settings
from json_utils import save_to_json
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer

def load_stories(directory):
    """
    function to read stories from text files.
    """
    json_filepath = "./stories.json"
    stories = []
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            filepath = os.path.join(directory, filename)
            loader = TextLoader(filepath, encoding='utf-8')
            documents = loader.load()
            
            # Extract story title from filename (remove .txt)
            story_title = os.path.splitext(filename)[0]
            
            # Combine document contents
            full_text = " ".join([doc.page_content for doc in documents])
            
            stories.append({
                'title': story_title,
                'content': full_text
            })

            save_to_json(stories,json_filepath)
    
    return stories


def compute_embeddings(stories: List[Dict[str, Any]], 
                        persist_directory: str = './chroma_db'):
    
    # Check if the directory exists; if not, create it
    if not os.path.exists(persist_directory):
        os.makedirs(persist_directory)
        print(f"Created directory: {persist_directory}")
    else:
        print(f"vector database Directory '{persist_directory}' already exists.")
        return

    # Initialize embedding model
    model = SentenceTransformer("all-MiniLM-L6-v2")
    # model = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # Initialize ChromaDB client
    chroma_client = chromadb.PersistentClient(
        path=persist_directory, 
        settings=Settings(anonymized_telemetry=False)
    )
    
    # Create or get collection
    collection = chroma_client.get_or_create_collection(name="stories")
    
    # Process and embed stories
    for story in stories:
        # Split story into chunks for better embedding
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, 
            chunk_overlap=200
        )
        
        # Split story content into chunks
        text_chunks = text_splitter.split_text(story['content'])
        
        # Embed and store chunks
        for chunk_idx, chunk in enumerate(text_chunks):
            # Generate embedding using Sentence Transformers
            embedding = model.encode(chunk).tolist()
            
            collection.add(
                embeddings=[embedding],
                documents=[chunk],
                metadatas=[{
                    'story_title': story['title'], 
                    'chunk_index': chunk_idx
                }],
                ids=[f"{story['title']}_{chunk_idx}"]
            )
    
    print(f"Embedded {len(stories)} stories in ChromaDB")


def main():
    stories = load_stories('./data')
    compute_embeddings(stories)

if __name__ == '__main__':
    main()