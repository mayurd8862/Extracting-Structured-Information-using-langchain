import streamlit as st
from json_utils import load_from_json, save_to_json
from get_character_info import extract_relevant_chunks, extract_titles, verify_character_in_story, extract_character_info

# Load stories
json_filepath = "./stories.json"
stories = load_from_json(json_filepath)

# Convert the list of dictionaries into a dictionary for quick access
content_dict = {item['title']: item['content'] for item in stories}

# Streamlit UI for user input
st.title("Character Info Extractor")
character = st.text_input("Enter the character name you want to search:")

if character:
    # Extract relevant chunks and metadata
    result = extract_relevant_chunks(character)
    metadata = result['metadatas']
    title_dict = extract_titles(metadata)
    
    info = None
    # Verify character and extract information
    for title in title_dict.keys():
        story = content_dict.get(title)
        if story and verify_character_in_story(story, character) == 1:
            info = extract_character_info(story, character)
            st.write(info)
            break
    else:
        st.error("The input character name is not found in any story!")
    
    # # Save character info to JSON file if found
    # if info:
    #     character_info_filepath = f"./{character}_info.json"
    #     save_to_json(info, character_info_filepath)
    #     st.success(f"Character info saved to {character_info_filepath}")
