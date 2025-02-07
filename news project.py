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
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert in detecting and removing bias in articles"},
                {"role": "user", "content": f"Summarize the following multiple news articles into a single unbiased report. Don't create any new information or assumptions on your own. Ensure that all the facts are present: {combined_content}"}
            ]
        )
        print(response)
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return "Summary unavailable."

def job():
    print("chala")
    combined_content = ["The x party always does this, 3 people died", "The x party is innocent, only 3 people died", "Cricketer takes 4 wickets"]
    # for url in sources:
    #     #parse the content
    #     combined_content.append(response.json().get("description"))
    
    embeddings = embedding_model.encode(combined_content)
    clusters=[]

    for i, content in enumerate(combined_content):
        added = False
        for cluster in clusters:
            print(cluster["index"])
            print(type(cluster["index"]))
            similarity = np.dot(embeddings[i], embeddings[cluster["index"]]) / (np.linalg.norm(embeddings[i]) * np.linalg.norm(embeddings[cluster["index"]]))
            if similarity > 0.8:  # Threshold for merging articles
                cluster["content"]+content
                added = True
                break

        if added == False:
            clusters.append({"index": i, "content": content})
            print(type(clusters))
    
    for cluster in clusters:
        summary = summarise(cluster["content"])
        articles.append(Article(content=summary))

    print(articles)

    


schedule.every().day.at("19:51").do(job)

while 1:
    schedule.run_pending()
    time.sleep(1)