import pandas as pd
from tqdm import tqdm
import os
from langchain_core.documents import Document
from datetime import date, timedelta
from langchain.prompts.chat import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
import pickle

# Load gemini API key
with open('/Users/vineethguptha/fhlbsf/gemini_api_key.pickle', 'rb') as handle:
    gemini_api_key = pickle.load(handle)

# Set gemini API key in the environment
os.environ["GOOGLE_API_KEY"] = gemini_api_key

# Initialize gemini embeddings
gemini_embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# Load data
data = pd.read_csv('results/Federal Home Loan Bank of San Francisco.csv')

# Filter out unrelated content
data = data[data['summaries'] != 'Not-related content.']
data = data[data['summaries'] != 'Not-related content']
data.reset_index(inplace=True)

# Convert publish_date to datetime
data['publish_date'] = pd.to_datetime(data['published date']).dt.date

# Sort data by publish_date
data.sort_values('publish_date', ascending=False, inplace=True)

# Read topics from file
with open('topics.txt', 'r') as f:
    topics = [line.strip() for line in f]

# Define quarter, month, and week dates
today = date.today()
quarter_date = today - timedelta(days=120)
month_date = today - timedelta(days=30)
week_date = today - timedelta(days=7)

# Define date filters
date_filters = {"Weekly": week_date, "Monthly": month_date, "Quarterly": quarter_date}

# Loop over topics
for topic in topics:
    print(f"Processing topic: {topic}")

    # Iterate over date filters
    for period, filter_date in date_filters.items():
        print(f"Processing for {period} period")

        # Filter data for current period
        filtered_data = data[data['publish_date'] > filter_date]

        # Initialize lists to store documents and metadata
        documents = []
        metadatas = []

        # Iterate over filtered data
        for ind, row in tqdm(filtered_data.iterrows()):
            # Create document
            doc = Document(page_content=row['content'], metadata=dict(publisher=row['publisher'], date=row['publish_date'],
                                                                      url=row['url'], title=row['title'],
                                                                      sentiment=row['default_sentiment']))
            # Append document and metadata to lists
            documents.append(doc)
            metadatas.append(dict(publisher=row['publisher'], date=row['publish_date'], url=row['url'], title=row['title'],
                                  sentiment=row['default_sentiment']))

        # Create FAISS index
        db = FAISS.from_documents(documents, gemini_embeddings)

        # Initialize list to store summaries for current period
        summaries_period = []

        # Iterate over filtered data
        for ind, row in tqdm(filtered_data.iterrows()):
            # Perform summarization process
            summarization_prompt = create_summarization_prompt(row['content'], topic)
            llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=gemini_api_key, temperature=0, top_p=1)
            summarizer_chain = summarization_prompt | llm | StrOutputParser()
            summary = summarizer_chain.invoke({"topic": topic, "content": row['content']})

            # Append summary to list
            summaries_period.append(summary)

            # Do something with the summary, e.g., save it to a file or database
            print(summary)

        # Create DataFrame for summaries
        df = pd.DataFrame({'Summary': summaries_period})

        # Save DataFrame to CSV
        output_folder = "RAG_results"
        os.makedirs(output_folder, exist_ok=True)
        file_path = os.path.join(output_folder, f"{topic}_{period}.csv")
        df.to_csv(file_path, index=False)
