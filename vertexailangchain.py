# -*- coding: utf-8 -*-
"""VERTEXAILANGCHAIN.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ulNOXsOBlxjvti25Ak5uqlWf9vmQpjl_
"""

!pip install google-cloud-aiplatform --upgrade --user --quiet

from google.colab import auth as google_auth
google_auth.authenticate_user()

PROJECT_ID = "fundamento-copilot" # @param {type:"string"}
LOCATION = "us-central1"  # @param {type:"string"}

from google.cloud import aiplatform
aiplatform.init(project=PROJECT_ID, location=LOCATION)

# from vertexai.preview.language_models import TextGenerationModel, TextEmbeddingModel
# model = TextGenerationModel.from_pretrained("text-bison@001")



# response1 = model.predict(
#       '''
#          Explain the theory of relativity in simple terms.

#       ''',
#     temperature=0.2,
#     max_output_tokens=256,
#     top_k=40,
#     top_p=.95)

# print(response1)

!pip install langchain
!pip install --upgrade --quiet langchain langchain-google-vertexai
!pip install PyPDF2
!pip install faiss-cpu
!pip install tiktoken

from PyPDF2 import PdfReader
from langchain_google_vertexai import VertexAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS

# import pandas as pd

# # Load the CSV file into a DataFrame
# file_path = '/content/chatDatabaseProd.media_woncore.csv'
# df = pd.read_csv(file_path)

# # Specify the column name from which you want to extract text
# column_name = 'translation'

# # Extract text from the specified column
# text_data = df[column_name].astype(str).tolist()

# # Concatenate all the text into a single string
# raw_text = ' '.join(text_data)

# raw_text

pdfreader = PdfReader('/content/Byte - downloads.pdf')

from typing_extensions import Concatenate
# read text from pdf
raw_text = ''
for i, page in enumerate(pdfreader.pages):
    content = page.extract_text()
    if content:
        raw_text += content

# We need to split the text using Character Text Split such that it should not increse token size
text_splitter = CharacterTextSplitter(
    separator = "/n",
    chunk_size = 800,
    chunk_overlap  = 200,
    length_function = len,
)
texts = text_splitter.split_text(raw_text)

embeddings = VertexAIEmbeddings()

document_search = FAISS.from_texts(texts, embeddings)

from langchain.chains.question_answering import load_qa_chain
from langchain.llms import VertexAI

chain = load_qa_chain(VertexAI(), chain_type="stuff")

# question = ['Can you provide more information about the training on stock market and share market?',
#             'Is prior experience required to participate in the online trading platform?',
# 'Can the trading be done using a mobile phone or laptop?',
# 'How does CFD trading work?',
# 'Can you connect me to a broker for more information?',
# 'What is the time commitment required for trading?',
# 'How long has the customer been in UAE?',
# 'Can you provide a promo code for any benefits on starting the training?',
# 'Can you explain the different types of trading platforms available with Woncore?',
# 'What is the process for allotting a broker to a customer?'
# ]

query = "Give me all possible questions from the document"
docs = document_search.similarity_search(query)
print(chain.run(input_documents=docs, question=query))