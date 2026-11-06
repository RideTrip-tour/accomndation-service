from fastapi import APIRouter, HTTPException, status

router = APIRouter(
    prefix="/api/accommodation/references",
    tags=["References"],
)


def raise_not_found():
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Страница не найдена",
    )


@router.get("/meal-types")
async def get_meal_types():
    raise_not_found()


@router.get("/accomm-types")
async def get_accommodation_types():
    raise_not_found()


@router.get("/amenities")
async def get_amenities():
    raise_not_found()
