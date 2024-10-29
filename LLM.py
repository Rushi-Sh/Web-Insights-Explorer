from langchain_huggingface import HuggingFaceEndpoint
from dotenv import load_dotenv
import os

load_dotenv()

sec_key = os.getenv("API_KEY")
repo_id = os.getenv("REPO_ID")


llm = HuggingFaceEndpoint(
    repo_id=repo_id,
    max_length=128,           
    temperature=0.5,          
    api_key=sec_key           
)


template1 = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {user_query}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)

template2 = (
    "Extract only the specific information from the text content below. "
    "Strictly follow these guidelines:\n\n"
    "1. **Extracted Information:** Retrieve only what directly matches the requested information: {user_query}. "
    "2. **No Additional Text:** Avoid adding any interpretations, comments, or explanations. "
    "3. **Return Format:** If no relevant information is found, return an empty string (''). "
    "4. **Data Precision:** Output exactly and only the specified data, without any other text."
    "\n\n"
    "Content:\n{dom_content}"
)


def get_ai_response(user_query,dom_chunks):

    parsed_results = []
    
    try:
        for i, chunk in enumerate(dom_chunks, start=1):
            prompt = template2.format(user_query=user_query, dom_content=chunk)
            response = llm.invoke(prompt)
            print(f"Parsed batch: {i} of {len(dom_chunks)}")
            
            parsed_results.append(response)
        
        return "\n".join(parsed_results)
    
    except Exception as e:
        print(f"Error: {e}")
        return ""  

