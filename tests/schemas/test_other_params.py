import pytest
from pydantic import ValidationError

from app.schemas.accommodation import (
    AccommodationOffersParams,
    AccommodationReviewsParams,
    AccommodationSearchParams,
    AccommodationSuggestParams,
    AccommodationTopOffersParams,
)
from app.utils.enums import HotelOrder


# Suggest
def test_suggest_params_valid():
    result = AccommodationSuggestParams(query="  London  ")

    assert result.query == "London"


@pytest.mark.parametrize("query", ["", " "])
def test_suggest_params_invalid(query):
    with pytest.raises(ValidationError):
        AccommodationSuggestParams(query=query)


# Search
def test_search_params_valid(valid_search_params):
    result = AccommodationSearchParams(**valid_search_params)

    assert result.location_id == 1
    assert result.adults == 2
    assert result.order_by == HotelOrder.RELEVANCE_DESC


@pytest.mark.parametrize(
    "bbox",
    [
        "10,20~30,40",
        "-10.5,-20.5~30.5,40.5",
        "-180,-90~180,90",
    ],
)
def test_search_params_valid_bbox(valid_search_params, bbox):
    result = AccommodationSearchParams(**valid_search_params, bbox=bbox)

    assert result.bbox == bbox


@pytest.mark.parametrize(
    "bbox",
    [
        "",
        "10,20",
        "abc,20~30,40",
        "181,20~30,40",
        "10,91~30,40",
        "30,20~10,40",
    ],
)
def test_search_params_invalid_bbox(valid_search_params, bbox):
    with pytest.raises(ValidationError):
        AccommodationSearchParams(**valid_search_params, bbox=bbox)


@pytest.mark.parametrize(
    "params",
    [
        {"images_limit": 21},
        {"order_by": "invalid"},
    ],
)
def test_search_params_invalid(valid_search_params, params):
    with pytest.raises(ValidationError):
        AccommodationSearchParams(**valid_search_params, **params)


# Offers
def test_offers_params_valid(valid_dates, valid_guests):
    result = AccommodationOffersParams(
        **valid_dates,
        **valid_guests,
        children_ages=[5, 10],
    )

    assert result.adults == 2
    assert result.children_ages == [5, 10]


# Reviews
def test_reviews_params_valid():
    result = AccommodationReviewsParams(limit=10, offset=5)

    assert result.limit == 10
    assert result.offset == 5


# Top Offers
def test_top_offers_params_valid(valid_dates):
    result = AccommodationTopOffersParams(
        **valid_dates,
        hotel_ids=["hotel-1", "hotel-2"],
    )

    assert result.hotel_ids == ["hotel-1", "hotel-2"]


@pytest.mark.parametrize("hotel_ids", [[], None])
def test_top_offers_params_invalid(valid_dates, hotel_ids):
    with pytest.raises(ValidationError):
        AccommodationTopOffersParams(
            **valid_dates,
            hotel_ids=hotel_ids,
        )


# Extra fields
def test_accommodation_schemas_forbid_extra_fields(all_schemas):
    for schema, valid_data in all_schemas.items():
        with pytest.raises(ValidationError):
            schema.model_validate(
                {
                    **valid_data,
                    "unexpected_field": "value",
                }
            )
