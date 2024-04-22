import os
import pickle
import string
import getpass
import pandas as pd
from tqdm import tqdm
from langchain.prompts.chat import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI


def create_sentiment_classification_prompt(topic):
    """
    Create a sentiment classification prompt based on the given topic.

    Args:
        topic (str): The topic for which the prompt is created.

    Returns:
        ChatPromptTemplate: The generated prompt template.
    """
    sentiment_classification_template = """
    This is the text. Based on the text, deterministically determine and
    strictly assign the sentiment label for the {topic} for the text whether
    it comes under category of negative or positive or neutral or not directly
    related. If you don't know the answer, just say that you don't know.
    The text should definitely have one category assigned.
    """.format(topic=topic)
    sentiment_prompt = ChatPromptTemplate.from_template(
        sentiment_classification_template)
    return sentiment_prompt


def create_summarization_prompt(content, topic):
    """
    Create a summarization prompt based on the given content and topic.

    Args:
        content (str): The content of the news article.
        topic (str): The topic for which the summary is created.

    Returns:
        ChatPromptTemplate: The generated prompt template.
    """
    summarization_template = """
    This is the news article content {content}.
    Extract the sentences from this news article related to the {topic}
    and summarize this content related to the {topic} into 30 words such
    that whole article is convered within these 30 words. Strictly restrict
    to this content only. Please avoid anything that is not related to this
    content. If the content is not related to the {topic},
    just return Not-related content.
    """.format(content=content, topic=topic)
    summarization_prompt = ChatPromptTemplate.from_template(
        summarization_template)
    return summarization_prompt


if __name__ == '__main__':
    with open('gemini_api_key.pickle', 'rb') as handle:
        gemini_api_key = pickle.load(handle)
    llm = ChatGoogleGenerativeAI(model="gemini-pro",
                                 google_api_key=gemini_api_key,
                                 temperature=0, top_p=1)
    output_parser = StrOutputParser()
    topics = []
    with open('topics.txt', 'r') as f:
        for line in f:
            topics.append(line.strip())
    for topic in topics:
        sentiment_prompt = create_sentiment_classification_prompt(topic)
        sentiment_chain = sentiment_prompt | llm | output_parser
        data = pd.read_csv(f'/news/{topic}.csv')
        texts = data['content'].values
        results = []
        for i in tqdm(range(len(texts))):
            result = sentiment_chain.invoke(
                {"texts": f"{texts[i: i+5]}", "topic": topic,
                 'total_number_of_texts': len(texts[i:i+5])})
            result = ''.join(i for i in result if not i.isdigit())
            result = ''.join(' ' if c in string.punctuation
                             else c for c in result)
            split_results = [i.strip() for i in result.split('\n')]
            results.extend(split_results)
        data['text sentiment'] = results

        summaries = []
        for ind, row in tqdm(data.iterrows()):
            summarization_prompt = create_summarization_prompt()
            summarizer_chain = summarization_prompt | llm | output_parser
            summaries.append(summarizer_chain.invoke(
                {"topic": topic, "content": row['content']}))
        data['summaries'] = summaries
        data.to_csv(f'/results/{topic}.csv', index=False)
