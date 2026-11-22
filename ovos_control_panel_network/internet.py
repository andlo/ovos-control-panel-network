"""Whether the device is online, from ovos-PHAL-plugin-connectivity-events.

``ovos.PHAL.internet_check`` drives the plugin to answer on
``mycroft.internet.state`` and ``mycroft.network.state`` (each
``{"state": "connected"|"disconnected"}``); both come back for one check, so
both are listened for and merged into one result.
"""
from __future__ import annotations

from typing import Any

#: How long the check may take.
DEFAULT_TIMEOUT = 5.0


def connectivity(bus) -> dict[str, Any]:
    """Report ``{"internet": "connected"|"disconnected"|None, "network": ...}``.

    Drives ``ovos-PHAL-plugin-connectivity-events`` with ``ovos.PHAL.internet_check``
    and listens for both ``mycroft.internet.state`` and ``mycroft.network.state``,
    since a single check answers on both topics. A value stays ``None`` when
    its topic never answered inside the timeout.
    """
    import threading

    from ovos_webui import buswait

    if not buswait.is_connected(bus):
        return {"internet": None, "network": None}

    def run():
        from ovos_bus_client.message import Message

        got = threading.Event()
        box: dict[str, Any] = {}

        def make(key):
            def handler(message):
                box[key] = (message.data or {}).get("state")
                if "internet" in box and "network" in box:
                    got.set()
            return handler

        h_internet = make("internet")
        h_network = make("network")
        bus.on("mycroft.internet.state", h_internet)
        bus.on("mycroft.network.state", h_network)
        try:
            bus.emit(Message("ovos.PHAL.internet_check", {},
                             {"source": "ovos-webui"}))
            got.wait(DEFAULT_TIMEOUT)
        finally:
            try:
                bus.remove("mycroft.internet.state", h_internet)
                bus.remove("mycroft.network.state", h_network)
            except Exception:  # noqa: BLE001 # pragma: no cover
                pass
        return {"internet": box.get("internet"), "network": box.get("network")}

    result = buswait.call(run, timeout=DEFAULT_TIMEOUT + 1.0, default=None)
    if result is None:
        return {"internet": None, "network": None}
    return result
