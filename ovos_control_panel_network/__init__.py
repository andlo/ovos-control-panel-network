"""Network: whether the device is online, and its Wi-Fi, for ovos-control-panel.

A panel extension: the panel finds this page through the
``opm.control_panel.page`` entry point (see pyproject.toml and the panel's
docs/pages.md, "Panel extensions"). Wi-Fi is ovos-PHAL-plugin-network-manager's
(scan, join, leave, forget, over the ``ovos.phal.nm.*`` messages), the internet
check ovos-PHAL-plugin-connectivity-events'. Nothing here runs outside the
panel.

It was one of the panel's own pages until a device that needs no Wi-Fi setup
(on a cable, in a container, in a browser) no longer needed to carry it.
"""


def routes(r):
    # imported here, so reading PAGE needs no web framework
    from ovos_control_panel_network.api import routes as add
    add(r)


PAGE = {
    "api_version": 1,
    "id": "network",
    "path": "/network",
    "title": {"key": "nav.network", "label": "Network"},
    "group": "everyday",
    "order": 50,
    # Wi-Fi is the network-manager plugin's, the internet check the
    # connectivity plugin's: a device with neither has nothing to show here
    "needs": ["ovos-phal-plugin-network-manager", "ovos-PHAL-plugin-network-manager",
              "ovos-PHAL-plugin-connectivity-events"],
    "html": "page.html",
    "icon": "icon.svg",
    "heading": {"key": "hdr.network", "label": "Network"},
    "i18n": "i18n",
    "routes": routes,
}
