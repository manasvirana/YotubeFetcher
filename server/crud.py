from sqlalchemy.future import select
from sqlalchemy import desc
from server.models import Video

async def get_paginated_videos(db, skip: int = 0, limit: int = 10):
    query = select(Video).order_by(desc(Video.published_at)).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

async def save_videos(db, videos):
    for video in videos:
        db.add(video)
    await db.commit()
