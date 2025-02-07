import schedule
import time
import requests
from sentence_transformers import SentenceTransformer
import numpy as np

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def summarise():
    print()

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


        

    


schedule.every().day.at("01:00").do(job)

while 1:
    schedule.run_pending()
    time.sleep(1)