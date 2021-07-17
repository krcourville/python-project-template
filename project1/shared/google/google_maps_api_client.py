from dataclasses import dataclass
from enum import Enum
import os
from typing import Dict, Iterable, List, Optional

import httpx
from pydantic import BaseModel


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


class GeocodeStatus(str, Enum):
    OK = "OK"
    ZERO_RESULTS = "ZERO_RESULTS"
    OVER_DAILY_LIMIT = "OVER_DAILY_LIMIT"
    OVER_QUERY_LIMIT = "OVER_QUERY_LIMIT"
    REQUEST_DENIED = "REQUEST_DENIED"
    INVALID_REQUEST = "INVALID_REQUEST"
    UNKNOWN_ERROR = "UNKNOWN_ERROR"


class AddressComponent(BaseModel):
    long_name: str
    short_name: str
    types: List[AddressComponentType]


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


class GeocodeResponse(BaseModel):
    results: List[GeocodeResult]
    status: GeocodeStatus
    error_message: Optional[str] = None


@dataclass
class GoogleMapsApiClientConfig:
    api_key: str
    base_url = "https://maps.googleapis.com/maps/api"

    @staticmethod
    def default() -> "GoogleMapsApiClientConfig":
        return GoogleMapsApiClientConfig(api_key=os.environ.get("GOOGLE_MAPS_API_KEY"))


class GoogleMapsApiClientError(RuntimeError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class GoogleMapsApiClient:
    def __init__(self, config: GoogleMapsApiClientConfig = None) -> None:
        self._config = config or GoogleMapsApiClientConfig.default()
        self._http = httpx.Client(
            base_url=self._config.base_url, params={"key": self._config.api_key}
        )

    async def geocode(self, request: GeocodeRequest) -> GeocodeResponse:
        params = {"address": request.address}
        res = self._http.get("geocode/json", params=params)
        json = res.json()
        parsed = GeocodeResponse.parse_obj(json)
        if parsed.status != GeocodeStatus.OK:
            raise GoogleMapsApiClientError(
                f"Unexpected status: {parsed.status}. {parsed.error_message}"
            )
        return parsed

    def __enter__(self):
        pass

    def __exit__(self):
        self._http.close()
