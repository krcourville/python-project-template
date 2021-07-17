from dataclasses import dataclass
import os
from typing import TypeVar

import httpx

import shared.google.maps.models as m


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


TResponse = TypeVar("TResponse", bound=m.GoogleResponseBase)


def parse_response(response_type: TResponse, res: httpx.Response) -> TResponse:
    json = res.json()
    parsed = response_type.parse_obj(json)
    if parsed.status != m.ResponseStatus.OK:
        raise GoogleMapsApiClientError(
            f"Unexpected status: {parsed.status}. {parsed.error_message}"
        )
    return parsed


class GoogleMapsApiClient:
    def __init__(self, config: GoogleMapsApiClientConfig = None) -> None:
        self._config = config or GoogleMapsApiClientConfig.default()
        self._http = httpx.Client(
            base_url=self._config.base_url, params={"key": self._config.api_key}
        )

    async def geocode(self, request: m.GeocodeRequest) -> m.GeocodeResponse:
        params = {"address": request.address}
        res = self._http.get("geocode/json", params=params)
        return parse_response(m.GeocodeResponse, res)

    async def get_place_detail(
        self, request: m.PlaceDetailRequest
    ) -> m.PlaceDetailResponse:
        params = {"place_id": request.place_id, "fields": ",".join(request.fields)}
        res = self._http.get("place/details/json", params=params)
        return parse_response(m.PlaceDetailResponse, res)

    def __enter__(self):
        pass

    def __exit__(self):
        self._http.close()
