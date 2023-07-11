from langchain.llms import OpenAI
# from langchain.chains.summarize import load_summarize_chain
# from langchain.text_splitter import RecursiveCharacterTextSplitter
from utils import check_and_exit, get_api_key
check_and_exit("OPENAI_API_KEY")
print("OPENAI_API_KEY found")
openai_api_key=get_api_key()
llm = OpenAI(temperature=0, openai_api_key=openai_api_key)