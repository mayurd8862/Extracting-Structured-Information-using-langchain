import os
from typing import List, Dict, Any

import chromadb
from sentence_transformers import SentenceTransformer
from chromadb.config import Settings
from json_utils import load_from_json,save_to_json
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq

# Load environment variables
load_dotenv()

LANGCHAIN_API_KEY = os.environ.get("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = LANGCHAIN_API_KEY
os.environ["LANGCHAIN_PROJECT"] = "deepstack_assignment"

def extract_relevant_chunks(character_name: str, 
                            persist_directory: str = './chroma_db', 
                            model_name: str = 'all-MiniLM-L6-v2') -> Dict[str, Any]:
    """
    Extract character information from embedded stories.
    """
    # Initialize embedding model
    model = SentenceTransformer(model_name)
    
    # Initialize ChromaDB client
    chroma_client = chromadb.PersistentClient(
        path=persist_directory, 
        settings=Settings(anonymized_telemetry=False)
    )
    
    # Get collection
    collection = chroma_client.get_or_create_collection(name="stories")
    
    # Embed character name
    character_embedding = model.encode(character_name).tolist()
    
    # Search for character mentions
    results = collection.query(
        query_embeddings=[character_embedding],
        n_results=5  # Top 5 most relevant chunks
    )
    
    return results

def extract_titles(metadata):
    """
    Extract and count story titles from metadata.
    """
    title_counts = {}
    for sublist in metadata:
        for item in sublist:
            title = item['story_title']
            title_counts[title] = title_counts.get(title, 0) + 1

    sorted_title_counts = dict(sorted(title_counts.items(), key=lambda item: item[1], reverse=True))
    return sorted_title_counts

class CharacterVerification(BaseModel):
    """
    Structured model for character verification in a story.
    """
    character_present: int = Field(
        description="1 if character exists in the story, 0 if not",
        ge=0,  # Greater than or equal to 0
        le=1   # Less than or equal to 1
    )

def verify_character_in_story(story_text: str, character_name: str) -> int:
    """
    Verify if a character exists in a given story using LangChain and Groq.
    """
    output_parser = JsonOutputParser(pydantic_object=CharacterVerification)
    prompt = PromptTemplate(
        template="""
        Analyze the following story and determine if the character '{character_name}' is present.
        
        Story:
        {story_text}
        
        {format_instructions}
        
        Respond with 1 if the character is in the story, 0 if not.
        """,
        input_variables=["story_text", "character_name"],
        partial_variables={"format_instructions": output_parser.get_format_instructions()}
    )
    
    llm = ChatGroq(
        temperature=0,  # Most precise output
        model_name="llama3-8b-8192",
        api_key=os.getenv('GROQ_API_KEY')
    )
    
    chain = prompt | llm | output_parser
    
    try:
        result = chain.invoke({"story_text": story_text, "character_name": character_name})
        return result.get('character_present', 0)
    except Exception as e:
        print(f"Error in character verification: {e}")
        return 0

class CharacterInfo(BaseModel):
    """
    Structured model for character information in a story.
    """
    name: str = Field(description="Full name of the character")
    storyTitle: str = Field(description="Title of the story")
    summary: str = Field(description="Brief summary of the character's story")
    relations: list = Field(description="List of character's relationships with other characters in story")
    characterType: str = Field(description="Character's role in the story")

def extract_character_info(story_text: str, character_name: str) -> dict:
    """
    Extract detailed information about a character from a story.
    """
    output_parser = JsonOutputParser(pydantic_object=CharacterInfo)
    prompt = PromptTemplate(
        template="""
        Analyze the following story and extract comprehensive information about the character '{character_name}'.
        
        Story:
        {story_text}
        
        {format_instructions}
        
        Provide a detailed JSON response with:
        - Character's full name
        - Story title
        - Character's role and journey summary
        - The character's relationships with other characters in the story for example : 
        ("name": "Arya Stark", "relation": "Sister" ,
          "name": "Eddard Stark", "relation": "Father" )
        - Character type (protagonist, antagonist, side character, etc.)
        
        Dont add any extra field to the json format. If the character is not found, return an empty JSON object.
        """,
        input_variables=["story_text", "character_name"],
        partial_variables={"format_instructions": output_parser.get_format_instructions()}
    )
    
    llm = ChatGroq(
        temperature=0.7,  # Allow some creativity in summarization
        model_name="llama3-8b-8192",
        api_key=os.getenv('GROQ_API_KEY')
    )
    
    chain = prompt | llm | output_parser
    
    try:
        result = chain.invoke({"story_text": story_text, "character_name": character_name})
        return result
    except Exception as e:
        print(f"Error in character information extraction: {e}")
        return {}

def main():
    # Load stories

    # stories = load_stories("./data")
    json_filepath = "./stories.json"
    stories = load_from_json(json_filepath)
    
    # Convert the list of dictionaries into a dictionary for quick access
    content_dict = {item['title']: item['content'] for item in stories}
    
    # Get character name from user input
    character = input("\nEnter the character you want to search: ")
    
    # Extract relevant chunks
    result = extract_relevant_chunks(character)
    metadata = result['metadatas']
    title_dict = extract_titles(metadata)
    
    info = None
    # Verify character and extract information
    for title in title_dict.keys():
        story = content_dict.get(title)
        if story and verify_character_in_story(story, character) == 1:
            info = extract_character_info(story, character)
            print("\n",info,"\n")
            break
    else:
        print("\nThe input character name is not found in any story !!\n")

        # Save character info to JSON file if found
    if info:
        character_info_filepath = f"./{character}_info.json"
        save_to_json(info,character_info_filepath)

if __name__ == '__main__':
    main()
