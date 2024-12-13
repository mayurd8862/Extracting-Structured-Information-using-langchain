import os
import chromadb
from sentence_transformers import SentenceTransformer
from chromadb.config import Settings

def get_stories(folder_path):
    """
    Simple function to read stories from text files.
    """
    stories = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as file:
                content = file.read()
                stories.append({
                    'title': filename.replace('.txt', ''),
                    'text': content
                })
    return stories

def create_embeddings(stories, db_path='./chroma_db'):
    """
    Create embeddings for stories and store in ChromaDB.
    """
    # Initialize embedding model
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Initialize ChromaDB client
    chroma_client = chromadb.PersistentClient(
        path=db_path, 
        settings=Settings(anonymized_telemetry=False)
    )
    
    # Create or get collection
    collection = chroma_client.get_or_create_collection(name="stories")
    
    # Process and embed stories
    for story in stories:
        # Split story into chunks
        chunks = [
            story['text'][i:i+1000] 
            for i in range(0, len(story['text']), 1000)
        ]
        
        # Embed and store chunks
        for chunk_idx, chunk in enumerate(chunks):
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
    # Specify the directory containing story files
    stories_directory = './stories'
    
    # Get stories
    stories = get_stories(stories_directory)
    
    # Create embeddings
    create_embeddings(stories)

if __name__ == "__main__":
    main()