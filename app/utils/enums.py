from enum import Enum


class MealType(str, Enum):
    RO = "RO"
    BB = "BB"
    HB = "HB"
    FB = "FB"
    AI = "AI"


class AccommodationType(str, Enum):
    HOTEL = "hotel"
    HOSTEL = "hostel"
    CAMPING = "camping"
    TOURIST_RESORT = "tourist-resort"
    HOLIDAY_HOME = "holiday-home"
    SANATORIUM = "sanatorium"
    GLAMPING = "glamping"
    APARTMENT = "apartment"


class HotelRating(float, Enum):
    THREE = 3.0
    THREE_AND_HALF = 3.5
    FOUR = 4.0
    FOUR_AND_HALF = 4.5


class HotelOrder(str, Enum):
    RELEVANCE_DESC = "relevance-desc"
    RATING_DESC = "rating-desc"
    PRICE_ASC = "price-asc"
    PRICE_DESC = "price-desc"
