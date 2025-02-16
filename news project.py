import schedule
import time
import requests
from sentence_transformers import SentenceTransformer
import numpy as np
import openai
import threading
from openai import OpenAI
from pydantic import BaseModel
import uvicorn
from fastapi import FastAPI

client = OpenAI()
app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
articles=[]

class Article(BaseModel):
    content: str
    
def summarise(contents: list)->str:
    combined_content = "\n".join(contents)
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
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
    print("Running")
    
    combined_content = get_posts()
    #combined_content = ["TechCorp Inc. announced 10,000 layoffs on February 8, 2025, citing declining revenue and restructuring efforts. CEO John Smith stated that the decision was necessary to maintain long-term stability. Employees affected will receive severance packages. The layoffs impact multiple departments globally. TechCorps stock fell 3 fter the announcement.", "Once again, we witness the ruthless nature of corporate greed. TechCorp Inc., a company that once prided itself on innovation and employee well-being, has now turned its back on 10,000 hardworking individuals. CEO John Smith, in a predictable display of corporate detachment, vaguely justified this mass firing as a 'necessary restructuring effort.'But lets not be fooled—this isnt about survival. Its about profits. Despite reporting billions in revenue last quarter, TechCorp still chooses to trim the fat at the expense of loyal employees. As usual, Wall Street reacted, with stocks dipping a mere 3%, a blip that will soon be forgotten. The human cost? Families struggling, careers upended, and trust shattered. Yet executives will keep their bonuses. This isn’t just a TechCorp issue; it’s a systemic problem. When will we hold these corporations accountable? When will workers stop being treated as expendable? The silence is deafening."]

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
    
@app.get('/')
def get_news():
    return articles

schedule.every().day.at("15:07").do(job)

def run_scheduler():
    while 1:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
    uvicorn.run(app, port=8000)