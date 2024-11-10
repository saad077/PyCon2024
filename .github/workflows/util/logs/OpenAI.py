from langchain.chains import MapReduceDocumentsChain, ReduceDocumentsChain
from langchain.text_splitter import CharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
import os
import openai
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain_community.document_loaders import TextLoader
from langchain_community.chat_models import AzureChatOpenAI

class OpenAI:

    def __init__(self, ):
        pass

def load_document():
    # cwd = os.getcwd()
    loader = TextLoader('app.log')
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
    docs = text_splitter.split_documents(documents)
    return docs[:6]


def summarize_mapreduce_summary_version2():
    # Map
    llm = AzureChatOpenAI(
            openai_api_base="",
            openai_api_version="",
            deployment_name='gpt-4o',
            openai_api_key="",
            openai_api_type = "azure_ad",
            max_tokens=500)
    
    docs = load_document()
    # Map
    map_template = """The following text contain logs coming from an applciation
    {docs}
    Based on the logs, please find it out the error occured and the main cause and also point it out which line of which file where the issue occured
    Helpful Answer:"""
    map_prompt = PromptTemplate.from_template(map_template)
    map_chain = LLMChain(llm=llm, prompt=map_prompt)
    # Reduce
    reduce_template = """The following is set of summaries:
    {docs}
    Take these and distill it into a final, consolidated summary of the main error caused the failure of application. 
    Helpful Answer:"""
    reduce_prompt = PromptTemplate.from_template(reduce_template)
    # Run chain
    reduce_chain = LLMChain(llm=llm, prompt=reduce_prompt)

    # Takes a list of documents, combines them into a single string, and passes this to an LLMChain
    combine_documents_chain = StuffDocumentsChain(
        llm_chain=reduce_chain, document_variable_name="docs"
    )

    # Combines and iteratively reduces the mapped documents
    reduce_documents_chain = ReduceDocumentsChain(
        # This is final chain that is called.
        combine_documents_chain=combine_documents_chain,
        # If documents exceed context for `StuffDocumentsChain`
        collapse_documents_chain=combine_documents_chain,
        # The maximum number of tokens to group documents into.
        token_max=4000,
    )
    # Combining documents by mapping a chain over them, then combining results
    map_reduce_chain = MapReduceDocumentsChain(
        # Map chain
        llm_chain=map_chain,
        # Reduce chain
        reduce_documents_chain=reduce_documents_chain,
        # The variable name in the llm_chain to put the documents in
        document_variable_name="docs",
        # Return the results of the map steps in the output
        return_intermediate_steps=False,
    )

    text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=8000, chunk_overlap=0
    )
    split_docs = text_splitter.split_documents(docs)
    return map_reduce_chain.run(split_docs)

ret = summarize_mapreduce_summary_version2()
# Open the file in write mode and write the string
with open('report.txt', 'w') as file:
    file.write(ret)