from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import random

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all domains to access
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

REDDIT_URL = "https://www.reddit.com/r/LifeProTips/top.json?t=all&limit=10"

@app.get("/advice")
def get_random_advice():
    try:
        headers = {"User-Agent": "fastapi-advice-bot"}
        response = requests.get(REDDIT_URL, headers=headers)
        data = response.json()

        posts = data.get("data", {}).get("children", [])
        if not posts:
            return {"error": "No advice found"}

        random_post = random.choice(posts)["data"]

        title = random_post.get("title", "No title available")
        content = random_post.get("selftext", "No content available")
        post_url = f"https://reddit.com{random_post.get('permalink', '')}"

        return {
            "advice": title,
            "details": content,
            "source": post_url
        }

    except Exception as e:
        return {"error": str(e)}

def handler(req, res):
    return app
