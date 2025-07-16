from langchain_google_genai import ChatGoogleGenerativeAI

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from prompt_template import build_prompt
import json
from dotenv import load_dotenv

load_dotenv()

def generate_sql(nl_query: str, metadata_path="financial_metadata.json") -> str:
    with open(metadata_path, "r") as f:
        metadata = json.load(f)

    prompt_text = build_prompt(nl_query, metadata)

    llm_model = ChatGoogleGenerativeAI(model='gemini-2.0-flash')


    prompt = PromptTemplate(
        input_variables=["question"],
        template="{question}"
    )

    # print("prompt_text:", prompt_text)
    response = llm_model.invoke(prompt.format(question=prompt_text))
    # print("RAW RESPONSE:", response)
    # print("##############################################################################################################")

    return response.content.replace("sqlite","").replace("```","").strip()