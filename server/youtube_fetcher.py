import os
import asyncio
import logging
from datetime import datetime, timedelta
import httpx
from dateutil.parser import isoparse
from sqlalchemy.future import select
from server.models import Video
from server.database import SessionLocal

YOUTUBE_API_KEYS = os.getenv("YOUTUBE_API_KEYS", "").split(",")
SEARCH_QUERY = os.getenv("YOUTUBE_SEARCH_QUERY", "music")
FETCH_INTERVAL = int(os.getenv("FETCH_INTERVAL", 10))

logger = logging.getLogger(__name__)
last_fetch_time = datetime.utcnow() - timedelta(minutes=5)

async def fetch_videos():
    global last_fetch_time
    used_keys = set()

    while True:
        published_after = last_fetch_time.isoformat("T") + "Z"
        params = {
            "part": "snippet",
            "q": SEARCH_QUERY,
            "type": "video",
            "order": "date",
            "publishedAfter": published_after,
            "maxResults": 10,
        }

        for key in YOUTUBE_API_KEYS:
            if key in used_keys:
                continue
            params["key"] = key

            try:
                async with httpx.AsyncClient(timeout=10) as client:
                    response = await client.get("https://www.googleapis.com/youtube/v3/search", params=params)
                    data = response.json()

                    if response.status_code != 200:
                        logger.error(f"Failed with status {response.status_code} for key {key[:6]}...: {data}")
                        used_keys.add(key)
                        continue

                    
                    if "error" in data:
                        err_msg = data["error"].get("message", "Unknown error")
                        logger.warning(f"API key quota or error for key {key[:6]}...: {err_msg}")
                        used_keys.add(key)
                        continue

                    items = data.get("items", [])
                    logger.info(f"Fetched {len(items)} items using key {key[:6]}...")

                    videos = []
                    for item in items:
                        vid_id = item["id"].get("videoId")
                        snippet = item["snippet"]

                        if not vid_id:
                            continue  

                        video = Video(
                            id=vid_id,
                            title=snippet["title"],
                            description=snippet.get("description", ""),
                            published_at=isoparse(snippet["publishedAt"]),
                            thumbnail_url=snippet["thumbnails"]["default"]["url"],
                        )
                        videos.append(video)

                    async with SessionLocal() as db:
                        for video in videos:
                            exists_query = await db.execute(select(Video).where(Video.id == video.id))
                            if exists_query.scalars().first() is None:
                                db.add(video)
                        await db.commit()

                    last_fetch_time = datetime.utcnow()
                    used_keys.clear()
                    break  

            except Exception as e:
                logger.error(f"Exception during fetch with key {key[:6]}...: {e}")
                used_keys.add(key)

        if len(used_keys) == len(YOUTUBE_API_KEYS):
            logger.error("All API keys failed or exhausted, waiting before retrying...")
            used_keys.clear()  

        await asyncio.sleep(FETCH_INTERVAL)
