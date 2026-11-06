from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, Query, status

from app.schemas.accommodation import (
    AccommodationOffersParams,
    AccommodationReviewsParams,
    AccommodationSearchParams,
    AccommodationSuggestParams,
    AccommodationTopOffersParams,
)

router = APIRouter(
    prefix="/api/accommodation",
    tags=["accommodation"],
)


def raise_not_found():
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Страница не найдена",
    )


@router.get("/suggest")
async def suggest(
    params: Annotated[AccommodationSuggestParams, Query()],
):
    raise_not_found()


@router.get("/search")
async def search(
    params: Annotated[AccommodationSearchParams, Query()],
):
    raise_not_found()


@router.get("/top-offers")
async def get_top_offers(
    params: Annotated[AccommodationTopOffersParams, Query()],
):
    raise_not_found()


@router.get("/filters")
async def get_filters():
    raise_not_found()


@router.get("/{hotel_id}/images")
async def get_hotel_images(hotel_id: Annotated[str, Path(min_length=1)]):
    raise_not_found()


@router.get("/{hotel_id}/offers")
async def get_hotel_offers(
    hotel_id: Annotated[str, Path(min_length=1)],
    params: Annotated[AccommodationOffersParams, Query()],
):
    raise_not_found()


@router.get("/{hotel_id}/reviews")
async def get_hotel_reviews(
    hotel_id: Annotated[str, Path(min_length=1)],
    params: Annotated[AccommodationReviewsParams, Query()],
):
    raise_not_found()


@router.get("/{hotel_id}")
async def get_hotel(hotel_id: Annotated[str, Path(min_length=1)]):
    raise_not_found()
