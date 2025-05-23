from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import desc

from server.database import get_db
from server.models import Video
from server.schemas import VideoOut

router = APIRouter()

@router.get("/videos", response_model=List[VideoOut])
async def get_videos(q: str = None, sort: str = None, db: AsyncSession = Depends(get_db)):
    stmt = select(Video)
    if q:
        stmt = stmt.where(Video.title.ilike(f"%{q}%"))
    if sort == "published_at":
        stmt = stmt.order_by(desc(Video.published_at))

    result = await db.execute(stmt)
    videos = result.scalars().all()
    return videos
