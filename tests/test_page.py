"""The panel finds this page through its entry point and serves it."""
from ovos_webui import pages


def test_the_panel_finds_the_page_and_loads_it_cleanly():
    reg = pages.load()
    page = reg.by_id()["network"]
    assert page.package == "ovos-control-panel-network" and not page.builtin
    assert not [p for p in reg.problems if p.get("page") == "network"]


def test_the_page_asks_for_the_internet_check_where_it_is(token_client):
    token_client.headers["Authorization"] = "Bearer s3cret-token"
    got = token_client.get("/network")
    assert got.status_code == 200 and "/api/network/internet" in got.text
    paths = set(token_client.app.openapi()["paths"])
    assert "/api/network/internet" in paths and "/api/system/connectivity" not in paths
