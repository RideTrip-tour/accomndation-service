from datetime import UTC, datetime, timedelta

import pytest
from pydantic import ValidationError

from app.schemas.accommodation import (
    BaseAccommodationFilters,
    BaseDateParams,
    BaseGuestsParams,
    BaseLocationParams,
    BasePaginationParams,
    BaseSearchPaginationParams,
)
from app.utils.enums import AccommodationType, HotelRating, MealType


# Pagination
@pytest.mark.parametrize(
    "schema,params",
    [
        (BasePaginationParams, {"limit": 20, "offset": 5}),
        (BaseSearchPaginationParams, {"page_limit": 20, "page_token": "next"}),
    ],
)
def test_pagination_params_valid(schema, params):
    result = schema(**params)

    for key, value in params.items():
        assert getattr(result, key) == value


@pytest.mark.parametrize(
    "schema,params",
    [
        (BasePaginationParams, {"limit": 0}),
        (BasePaginationParams, {"limit": 101}),
        (BasePaginationParams, {"offset": -1}),
        (BaseSearchPaginationParams, {"page_limit": 0}),
        (BaseSearchPaginationParams, {"page_limit": 51}),
        (BaseSearchPaginationParams, {"page_token": ""}),
    ],
)
def test_pagination_params_invalid(schema, params):
    with pytest.raises(ValidationError):
        schema(**params)


# Location
@pytest.mark.parametrize("params", [{"location_id": 1}, {"geo_id": 123}])
def test_location_params_valid(params):
    result = BaseLocationParams(**params)

    assert result.model_dump(exclude_unset=True) == params


@pytest.mark.parametrize(
    "params",
    [
        {},
        {"location_id": 1, "geo_id": 123},
        {"location_id": 0},
        {"geo_id": -1},
    ],
)
def test_location_params_invalid(params):
    with pytest.raises(ValidationError):
        BaseLocationParams(**params)


# Dates
def test_date_params_valid():
    checkin = datetime.now(UTC).date() + timedelta(days=1)
    checkout = checkin + timedelta(days=5)

    result = BaseDateParams(
        checkin_date=checkin,
        checkout_date=checkout,
    )

    assert result.checkout_date > result.checkin_date


@pytest.mark.parametrize("days", [0, -1])
def test_date_params_invalid(days):
    checkin = datetime.now(UTC).date() + timedelta(days=1)

    with pytest.raises(ValidationError):
        BaseDateParams(
            checkin_date=checkin,
            checkout_date=checkin + timedelta(days=days),
        )


# Guests
def test_guests_params_valid():
    result = BaseGuestsParams(adults=2, children_ages=[5, 10])

    assert result.adults == 2
    assert result.children_ages == [5, 10]


@pytest.mark.parametrize(
    "params",
    [
        {},
        {"adults": 0},
        {"adults": -1},
        {"adults": 2, "children_ages": [-1]},
    ],
)
def test_guests_params_invalid(params):
    with pytest.raises(ValidationError):
        BaseGuestsParams(**params)


# Filters
def test_accommodation_filters_valid():
    result = BaseAccommodationFilters(
        min_price=1000,
        max_price=5000,
        meal_type=[MealType.BB, MealType.HB],
        stars=[3, 4, 5],
        min_rating=HotelRating.FOUR,
        accomm_type=[AccommodationType.HOTEL],
        wi_fi=True,
        pool=False,
    )

    assert result.min_price == 1000
    assert result.max_price == 5000
    assert result.stars == [3, 4, 5]


@pytest.mark.parametrize(
    "params",
    [
        {"min_price": -1},
        {"min_price": 5000, "max_price": 1000},
        {"stars": []},
        {"stars": [0]},
        {"stars": [6]},
    ],
)
def test_accommodation_filters_invalid(params):
    with pytest.raises(ValidationError):
        BaseAccommodationFilters(**params)
