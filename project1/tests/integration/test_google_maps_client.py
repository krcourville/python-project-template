import pytest

from shared.google.google_maps_api_client import (
    GoogleMapsApiClient,
    GeocodeRequest,
    GeocodeStatus,
)

@pytest.fixture
def sut() -> GoogleMapsApiClient:
    return GoogleMapsApiClient()


@pytest.mark.asyncio
async def test_geocode_address(sut: GoogleMapsApiClient):
    request = GeocodeRequest(address="200 E Colfax Ave, Denver, CO 80203")
    res = await sut.geocode(request)
    assert res.status == GeocodeStatus.OK
    assert len(res.results) == 1
    result = res.results[0]
    assert result.formatted_address == "200 E Colfax Ave, Denver, CO 80203, USA"
