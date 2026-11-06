from datetime import date as Date
from re import fullmatch

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.schemas.constants import (
    DEFAULT_IMAGES_LIMIT,
    DEFAULT_LIMIT,
    DEFAULT_OFFSET,
    DEFAULT_PAGE_LIMIT,
    MAX_IMAGES_LIMIT,
    MAX_LIMIT,
    MAX_PAGE_LIMIT,
    MAX_STARS,
    MIN_ADULTS,
    MIN_ID,
    MIN_IMAGES_LIMIT,
    MIN_LIMIT,
    MIN_OFFSET,
    MIN_PAGE_LIMIT,
    MIN_PRICE,
    MIN_STARS,
)
from app.utils.enums import AccommodationType, HotelOrder, HotelRating, MealType


class BaseAccommodationParams(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )


class BasePaginationParams(BaseAccommodationParams):
    limit: int = Field(
        default=DEFAULT_LIMIT,
        ge=MIN_LIMIT,
        le=MAX_LIMIT,
    )
    offset: int = Field(
        default=DEFAULT_OFFSET,
        ge=MIN_OFFSET,
    )


class BaseSearchPaginationParams(BaseAccommodationParams):
    page_limit: int = Field(
        default=DEFAULT_PAGE_LIMIT,
        ge=MIN_PAGE_LIMIT,
        le=MAX_PAGE_LIMIT,
    )
    page_token: str | None = Field(
        default=None,
        min_length=1,
    )


class BaseLocationParams(BaseAccommodationParams):
    location_id: int | None = Field(default=None, ge=MIN_ID)
    geo_id: int | None = Field(default=None, ge=MIN_ID)

    @model_validator(mode="after")
    def validate_location(self):
        if (self.location_id is None) == (self.geo_id is None):
            raise ValueError("Provide either location_id or geo_id")

        return self


class BaseDateParams(BaseAccommodationParams):
    checkin_date: Date
    checkout_date: Date

    @model_validator(mode="after")
    def validate_dates(self):
        if self.checkout_date <= self.checkin_date:
            raise ValueError("checkout_date must be later than checkin_date")

        return self


class BaseAccommodationFilters(BaseAccommodationParams):
    min_price: int | None = Field(default=None, ge=MIN_PRICE)
    max_price: int | None = Field(default=None, ge=MIN_PRICE)

    meal_type: list[MealType] | None = None
    stars: list[int] | None = Field(
        default=None,
        min_length=1,
        max_length=MAX_STARS,
    )

    nearby_sea: bool | None = None
    nearby_park: bool | None = None
    nearby_airport: bool | None = None

    wi_fi: bool | None = None
    air_conditioning: bool | None = None
    pool: bool | None = None
    car_park: bool | None = None
    spa: bool | None = None
    pets: bool | None = None
    sauna: bool | None = None
    bathhouse: bool | None = None
    restaurant: bool | None = None
    cafe: bool | None = None
    gym: bool | None = None
    transfer: bool | None = None

    min_rating: HotelRating | None = None
    accomm_type: list[AccommodationType] | None = None

    free_cancellation: bool | None = None
    is_corporate: bool | None = None

    @model_validator(mode="after")
    def validate_price_range(self):
        if (
            self.min_price is not None
            and self.max_price is not None
            and self.min_price > self.max_price
        ):
            raise ValueError("min_price cannot be greater than max_price")

        return self

    @model_validator(mode="after")
    def validate_stars(self):
        if self.stars is not None and any(
            star < MIN_STARS or star > MAX_STARS for star in self.stars
        ):
            raise ValueError(f"stars must be between {MIN_STARS} and {MAX_STARS}")

        return self


class BaseGuestsParams(BaseAccommodationParams):
    adults: int = Field(ge=MIN_ADULTS)
    children_ages: list[int] | None = None

    @model_validator(mode="after")
    def validate_children_ages(self):
        if self.children_ages is not None and any(
            age < 0 for age in self.children_ages
        ):
            raise ValueError("children ages cannot be negative")

        return self


class AccommodationSearchParams(
    BaseLocationParams,
    BaseDateParams,
    BaseSearchPaginationParams,
    BaseAccommodationFilters,
    BaseGuestsParams,
):
    bbox: str | None = None
    order_by: HotelOrder = HotelOrder.RELEVANCE_DESC
    hotel_id: str | None = Field(default=None, min_length=1)

    images_limit: int = Field(
        default=DEFAULT_IMAGES_LIMIT,
        ge=MIN_IMAGES_LIMIT,
        le=MAX_IMAGES_LIMIT,
    )

    @model_validator(mode="after")
    def validate_bbox(self):
        if self.bbox is None:
            return self

        pattern = (
            r"^-?\d+(?:\.\d+)?,-?\d+(?:\.\d+)?"
            r"~-?\d+(?:\.\d+)?,-?\d+(?:\.\d+)?$"
        )

        if fullmatch(pattern, self.bbox) is None:
            raise ValueError("bbox must have format minLon,minLat~maxLon,maxLat")

        min_lon, min_lat, max_lon, max_lat = (
            float(value) for pair in self.bbox.split("~") for value in pair.split(",")
        )

        if not (
            -180 <= min_lon <= 180
            and -180 <= max_lon <= 180
            and -90 <= min_lat <= 90
            and -90 <= max_lat <= 90
        ):
            raise ValueError("bbox coordinates are out of range")

        if min_lon > max_lon or min_lat > max_lat:
            raise ValueError("bbox minimum coordinates cannot exceed maximum")

        return self


class AccommodationSuggestParams(BaseAccommodationParams):
    query: str = Field(min_length=1)


class AccommodationOffersParams(BaseDateParams, BaseGuestsParams):
    pass


class AccommodationReviewsParams(BasePaginationParams):
    pass


class AccommodationTopOffersParams(
    BaseDateParams,
    BasePaginationParams,
):
    hotel_ids: list[str] = Field(min_length=1)
