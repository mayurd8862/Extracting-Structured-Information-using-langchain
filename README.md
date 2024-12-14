# Extracting Structured Information using Langchain

## 🎯  Objective
This project aims to extract structured details about characters from stories in a provided dataset and output the required details in JSON format. The script leverages embeddings for information retrieval and processing using MistralAI with LangChain. The goal is to transform unstructured narrative data into a structured format using embeddings and processing techniques. 

---

## 🤖 Tech Stack used:
- **python**
- **Groq** - A specialized AI accelerator designed for large language models, offering high performance and efficiency. used "mixtral-8x7b-32768" LLM model through groq.
- **Langchain** - used for documents loader, llm integration
- **Langsmith** - Monitoring and visualizing LLM calls, tokens, and other LLM parameters
- **git** - for version control system
- **pylint** - for ensuring code quality
- **Streamlit** - For user interface creation "IN PROGRESS"
  
## 🛠️ Installation 

1. Clone the Repository:
    ```bash
    git clone https://github.com/mayurd8862/Extracting-Structured-Information-using-langchain.git
    ```
2. Navigate to the project directory:
    ```bash
    cd Extracting-Structured-Information-using-langchain
    ```
    
3. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```

4. Install Dependencies:
    ```bash
    pip install -r requirements.txt
    ```
    
## 🔐 Setup API keys

- Create a .env file in the root directory of the project and add following api keys to it.
  
  ```bash
   LANGCHAIN_API_KEY = your_langchain_api_key
   GROQ_API_KEY = your_groq_api_key
   ```
  
## 🚀 Usage

1. **🔍 Compute Embeddings :**
Run the following command to compute embeddings for all story files and persist the data into the vector database:

```bash
python compute_embeddings.py compute-embeddings --data-dir data/
```

2. **🕵️ Get Character Information :**
Run the following command to retrieve structured details about a character:

```bash
python get_character_info.py get-character-info --character-name "Jon Snow"
```

---

## 🔬 Methodology





## 🌊 Workflow flowchart


## 👀 Monitoring LLM calls with LangSmith

LangSmith is a powerful platform designed to provide comprehensive visibility and control over your Large Language Model (LLM) calls within your agents.

1. **Login to LangSmith**: Visit the LangSmith website and enter your credentials to log in to your account.
2. **Go to Projects**: Once logged in, navigate to the "Projects" section of the LangSmith dashboard.
Locate the project(s) that you have integrated with LangSmith. You can identify them by their names or descriptions.
3. **Monitor LLM Call Flows**: Click on a specific project to view its details. Go to the Runs section and analyse llm calls and outputs
4. **visualize**: In the "Monitoring" section, you should see a visualization of the LLM call flows within that project.
The visualization will display the sequence of LLM calls, their relationships, and any dependencies between them.

[View LLM calls Tracing](https://smith.langchain.com/o/f602a986-7b0f-5e2b-aa00-74708f7af432/projects/p/93d14499-78a2-4f86-af16-5f0692deda87?timeModel=%7B%22duration%22%3A%227d%22%7D)

## 📧 Contact 
For any questions or suggestions, feel free to reach out:

- **Email**: mayur.dabade21@vit.edu
- **GitHub** : [mayurd8862](https://github.com/mayur8862)
- **LinkedIn** : [https://www.linkedin.com/in/mayur-dabade-b527a9230](https://www.linkedin.com/in/mayur-dabade-b527a9230)













