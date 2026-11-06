from datetime import UTC, datetime, timedelta

import pytest

from app.schemas.accommodation import (
    AccommodationOffersParams,
    AccommodationReviewsParams,
    AccommodationSearchParams,
    AccommodationSuggestParams,
    AccommodationTopOffersParams,
    BaseAccommodationFilters,
    BaseAccommodationParams,
    BaseDateParams,
    BaseGuestsParams,
    BaseLocationParams,
    BasePaginationParams,
    BaseSearchPaginationParams,
)


@pytest.fixture
def valid_dates():
    checkin = datetime.now(UTC).date() + timedelta(days=1)

    return {
        "checkin_date": checkin,
        "checkout_date": checkin + timedelta(days=4),
    }


@pytest.fixture
def valid_location():
    return {"location_id": 1}


@pytest.fixture
def valid_guests():
    return {"adults": 2}


@pytest.fixture
def valid_search_params(valid_dates, valid_location, valid_guests):
    return {
        **valid_dates,
        **valid_location,
        **valid_guests,
    }


@pytest.fixture
def all_schemas(valid_dates, valid_guests, valid_search_params, valid_location):
    return {
        BaseAccommodationParams: {},
        BasePaginationParams: {},
        BaseSearchPaginationParams: {},
        BaseLocationParams: valid_location,
        BaseDateParams: valid_dates,
        BaseAccommodationFilters: {},
        BaseGuestsParams: valid_guests,
        AccommodationSearchParams: valid_search_params,
        AccommodationSuggestParams: {"query": "London"},
        AccommodationOffersParams: {
            **valid_dates,
            **valid_guests,
        },
        AccommodationReviewsParams: {},
        AccommodationTopOffersParams: {
            **valid_dates,
            "hotel_ids": ["hotel-1"],
        },
    }
