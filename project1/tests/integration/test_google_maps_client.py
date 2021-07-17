import pytest

import shared.google.maps as gm


@pytest.fixture
def sut() -> gm.GoogleMapsApiClient:
    return gm.GoogleMapsApiClient()


@pytest.mark.asyncio
async def test_geocode_address(sut: gm.GoogleMapsApiClient):
    request = gm.GeocodeRequest(address="200 E Colfax Ave, Denver, CO 80203")
    res = await sut.geocode(request)
    assert res.status == gm.ResponseStatus.OK
    assert len(res.results) == 1
    result = res.results[0]
    assert result.formatted_address == "200 E Colfax Ave, Denver, CO 80203, USA"


@pytest.mark.asyncio
async def test_place_detail(sut: gm.GoogleMapsApiClient):
    request = gm.PlaceDetailRequest(
        place_id="ChIJzxcfI6qAa4cR1jaKJ_j0jhE",
        fields=[
            gm.PlaceDetailField.address_component,
            gm.PlaceDetailField.formatted_address,
        ],
    )
    res = await sut.get_place_detail(request)
    assert res.status == gm.ResponseStatus.OK
    assert res.result.formatted_address == "Denver, CO, USA"
