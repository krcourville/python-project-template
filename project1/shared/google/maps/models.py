from dataclasses import dataclass
from enum import Enum
from typing import Dict, Iterable, List, Optional

from pydantic import BaseModel


class ResponseStatus(str, Enum):
    OK = "OK"
    ZERO_RESULTS = "ZERO_RESULTS"
    OVER_DAILY_LIMIT = "OVER_DAILY_LIMIT"
    OVER_QUERY_LIMIT = "OVER_QUERY_LIMIT"
    REQUEST_DENIED = "REQUEST_DENIED"
    INVALID_REQUEST = "INVALID_REQUEST"
    UNKNOWN_ERROR = "UNKNOWN_ERROR"


class AddressComponentType(str, Enum):
    postal_code = "postal_code"
    locality = "locality"
    political = "political"
    administrative_area_level_2 = "administrative_area_level_2"
    administrative_area_level_1 = "administrative_area_level_1"
    country = "country"
    route = "route"
    street_number = "street_number"
    neighborhood = "neighborhood"
    premise = "premise"


class LocationType(str, Enum):
    APPROXIMATE = "APPROXIMATE"


class AddressComponent(BaseModel):
    long_name: str
    short_name: str
    types: List[AddressComponentType]


class GoogleResponseBase(BaseModel):
    status: ResponseStatus
    error_message: Optional[str] = None


@dataclass
class GeocodeRequest:
    """
    Required fields are either address OR components

    Reference: https://developers.google.com/maps/documentation/geocoding/overview#GeocodingRequests
    """

    address: Optional[str] = None
    components: Optional[dict] = None
    language: Optional[str] = None
    region: Optional[str] = None


class PlaceDetailField(str, Enum):
    address_component = "address_component"
    formatted_address = "formatted_address"


@dataclass
class PlaceDetailRequest:
    place_id: str
    fields: Iterable[PlaceDetailField]


class PlaceDetailResult(BaseModel):
    address_components: List[AddressComponent]
    formatted_address: str


class PlaceDetailResponse(GoogleResponseBase):
    result: PlaceDetailResult


class Coordinate(BaseModel):
    lat: float
    lng: float


class Geometry(BaseModel):
    location: Coordinate


class GeocodeResult(BaseModel):
    address_components: List[AddressComponent]
    formatted_address: str
    geometry: Geometry
    place_id: str
    types: List[AddressComponentType]


class GeocodeResponse(GoogleResponseBase):
    results: List[GeocodeResult]
