"""Test fixtures: the panel in a temporary sandbox, as the panel's own tests
run it. ``ovos_config`` resolves its paths when imported, so the XDG
variables are set before anything from OVOS is imported."""
import os
import tempfile

_SANDBOX = tempfile.mkdtemp(prefix="ovos-cp-network-tests-")
os.environ["XDG_CONFIG_HOME"] = os.path.join(_SANDBOX, "config")
os.environ["XDG_DATA_HOME"] = os.path.join(_SANDBOX, "data")
os.environ["XDG_CACHE_HOME"] = os.path.join(_SANDBOX, "cache")
os.environ["XDG_CONFIG_DIRS"] = os.path.join(_SANDBOX, "etc")
os.environ["OVOS_DEFAULT_CONFIG"] = os.environ.get("OVOS_DEFAULT_CONFIG", "")
os.makedirs(os.environ["XDG_CONFIG_HOME"], exist_ok=True)

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from ovos_webui.service import create_app  # noqa: E402


@pytest.fixture(autouse=True)
def reset_bus_gate():
    """The panel's bus gate is process wide, so a tripped breaker must not leak."""
    from ovos_webui import buswait
    buswait.GATE.reset_for_tests()
    yield
    buswait.GATE.reset_for_tests()


@pytest.fixture
def bus():
    from ovos_utils.fakebus import FakeBus
    return FakeBus()


@pytest.fixture
def client(bus):
    app = create_app(bus=bus, host="127.0.0.1", token=None, connect_bus=False)
    with TestClient(app, base_url="http://127.0.0.1:8500",
                    headers={"sec-fetch-site": "same-origin"}) as test_client:
        yield test_client


@pytest.fixture
def token_client(bus):
    app = create_app(bus=bus, host="0.0.0.0", token="s3cret-token", connect_bus=False)
    with TestClient(app, base_url="http://127.0.0.1:8500",
                    headers={"sec-fetch-site": "same-origin"}) as test_client:
        yield test_client
