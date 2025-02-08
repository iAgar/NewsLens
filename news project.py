import schedule
import time
import requests
from sentence_transformers import SentenceTransformer
import numpy as np
import openai
from openai import OpenAI
from pydantic import BaseModel

client = OpenAI()

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
articles=[]

class Article(BaseModel):
    content: str
    
def summarise(contents: list)->str:
    combined_content = "\n".join(contents)
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are an expert in detecting and removing bias in articles"},
                {"role": "user", "content": f"Summarize the following multiple news articles into a single unbiased report. Don't create any new information or assumptions on your own. Ensure that all the facts are present: {combined_content}"}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return "Summary unavailable."

def get_posts():
    combined_content=[]
    api_key='api_live_DhnggeJIBMu06ak83Zog3J8yzpwe3rAGuu8ud0IqT8Akh'
    sites=['cnn.com','ndtv.com','nytimes.com','hindustantimes.com']
    url='https://api.apitube.io/v1/news/top-headlines?api_key='+api_key+'&per_page=5&page=1&source.domain='
    for site in sites:
        response = requests.post(url+site)
        if response.status_code == 200:
            posts = response.json()
            for res in posts["results"]:
                combined_content.append(res["body"])
        else:
            continue
    
    return combined_content


def job():
    print("chala")
    
    combined_content = get_posts()
    
    embeddings = embedding_model.encode(combined_content)
    clusters=[]

    for i, content in enumerate(combined_content):
        added = False
        for cluster in clusters:
            similarity = np.dot(embeddings[i], embeddings[cluster["index"]]) / (np.linalg.norm(embeddings[i]) * np.linalg.norm(embeddings[cluster["index"]]))
            if similarity > 0.8:  # Threshold for merging articles
                cluster["content"]+content
                added = True
                break

        if added == False:
            clusters.append({"index": i, "content": content})
    
    for cluster in clusters:
        summary = summarise(cluster["content"])
        articles.append(Article(content=summary))

    print(articles)

    


schedule.every().day.at("12:56").do(job)

while 1:
    schedule.run_pending()
    time.sleep(1)