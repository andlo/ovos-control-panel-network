"""The internet check, against a stand-in connectivity-events plugin."""


def _connectivity_bus(*, internet="connected", network="connected", answer=True):
    from ovos_bus_client.message import Message
    from ovos_utils.fakebus import FakeBus

    bus = FakeBus()
    if answer:
        def on_check(m):
            bus.emit(Message("mycroft.internet.state", {"state": internet}, m.context))
            bus.emit(Message("mycroft.network.state", {"state": network}, m.context))
        bus.on("ovos.PHAL.internet_check", on_check)
    return bus


def test_connectivity_parses_both_states():
    from ovos_control_panel_network import internet as system
    r = system.connectivity(_connectivity_bus(internet="connected", network="connected"))
    assert r == {"internet": "connected", "network": "connected"}

    r = system.connectivity(_connectivity_bus(internet="disconnected", network="disconnected"))
    assert r == {"internet": "disconnected", "network": "disconnected"}


def test_connectivity_timeout_reports_unknown():
    from ovos_utils.fakebus import FakeBus
    from ovos_control_panel_network import internet as system

    system.DEFAULT_TIMEOUT = 0.3
    assert system.connectivity(FakeBus()) == {"internet": None, "network": None}
    system.DEFAULT_TIMEOUT = 5.0
