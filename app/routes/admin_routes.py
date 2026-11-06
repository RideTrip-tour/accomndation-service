from fastapi import APIRouter, HTTPException, status

router = APIRouter(
    prefix="/api/admin/accommodation",
    tags=["Admin"],
)


def raise_not_found():
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Страница не найдена",
    )


@router.post("/feed/sync")
async def sync_feed():
    raise_not_found()


@router.get("/feed/status")
async def get_feed_status():
    raise_not_found()


@router.get("/cache/stats")
async def get_cache_stats():
    raise_not_found()
