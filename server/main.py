import os
import requests
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from typing import Optional
import asyncio
from server.utils import APIKeyRotator 

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEYS = os.getenv("YOUTUBE_API_KEY", "").split(",")
key_rotator = APIKeyRotator(API_KEYS)

YOUTUBE_API_URL = "https://www.googleapis.com/youtube/v3/search"

@app.get("/videos")
async def get_videos(
    search: Optional[str] = Query(None, description="Search keyword"),
    page_size: int = 10,
    sort: str = "desc"
):
    if not search:
        return {"error": "Search query is required to fetch new data."}
    for _ in range(len(API_KEYS)):
        api_key = await key_rotator.get_key()

        params = {
            "part": "snippet",
            "q": search,
            "type": "video",
            "maxResults": page_size,
            "order": "date" if sort == "desc" else "relevance",
            "key": api_key,
        }

        try:
            response = requests.get(YOUTUBE_API_URL, params=params)
            response.raise_for_status()
            data = response.json()

            videos = []
            for item in data.get("items", []):
                video = {
                    "id": item["id"]["videoId"],
                    "title": item["snippet"]["title"],
                    "description": item["snippet"]["description"],
                    "publishedAt": item["snippet"]["publishedAt"],
                    "thumbnails": item["snippet"]["thumbnails"],
                }
                videos.append(video)

            return {
                "videos": videos,
                "total": len(videos)
            }

        except requests.HTTPError as e:
            if response.status_code == 403: 
                await key_rotator.rotate_key() 
                continue
            raise HTTPException(status_code=502, detail=f"Failed to fetch from YouTube: {e}")

    
    raise HTTPException(status_code=502, detail="All API keys quota exceeded or invalid.")
