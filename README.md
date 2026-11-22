# ovos-control-panel-network

The Network page for
[ovos-control-panel](https://github.com/OpenVoiceOS/ovos-control-panel):
whether the device is online, the Wi-Fi networks near it, and joining,
leaving or forgetting one.

It is a **panel extension**: a page for the panel, nothing more. It was one of
the panel's own pages up to 0.0.1a86; it left so that a device that needs no
Wi-Fi setup (on a cable, in a container, in a browser) does not carry it.
Install it beside the panel:

```
pip install --pre ovos-control-panel-network
```

(`--pre`, as for the panel itself.) Then restart the panel. Wi-Fi needs
`ovos-PHAL-plugin-network-manager` on the device, the internet check
`ovos-PHAL-plugin-connectivity-events`.

## The page

The Network page shows whether the device is online, shows the Wi-Fi networks
near it, and lets you join, leave, or forget one.

![The Network page](docs/img/network-wide.png)

![The same page on a phone](docs/img/network-mobile.png)

## What it needs

The Wi-Fi part needs the `ovos-PHAL-plugin-network-manager` plugin, installed
and running on the device. Install it on the [Plugins](https://github.com/OpenVoiceOS/ovos-control-panel/blob/dev/docs/plugins.md) page.
Without it, the page shows a message that the plugin is missing instead of
a network list. The internet status needs
`ovos-PHAL-plugin-connectivity-events`.

## Read it top to bottom

The page has three parts, in this order:

1. **Internet**: whether the device is on a network and can reach the
   internet. Press **Refresh** to check again.
2. **Current network** — the network the device is connected to now, with
   **Disconnect** and **Forget this network** buttons.
3. **Available networks** — every network the device can reach, found by
   the last scan. Press **Scan** to look again. Each network shows its name
   and its security type exactly as `nmcli` reports it, such as `WPA2` or
   `WPA2 WPA3`. An open network reports nothing at all, and the page shows it
   as needing no password.

Press a network in the list to join it. If it needs a password, the page
asks for one before it connects.

## Before you switch networks

Switching Wi-Fi can drop the device's own connection, and your browser's
connection to the device too, if your browser is on the same network. The
page warns you of this before it switches. If the page stops responding
after a switch, reconnect your own device to the network you chose, then
open the page again.

## If it doesn't work

If the plugin shows as missing, install `ovos-PHAL-plugin-network-manager`
on the [Plugins](https://github.com/OpenVoiceOS/ovos-control-panel/blob/dev/docs/plugins.md) page and restart the PHAL service. If a scan
finds no networks, wait a few seconds and press **Scan** again. For
anything else, see [troubleshooting.md](https://github.com/OpenVoiceOS/ovos-control-panel/blob/dev/docs/troubleshooting.md).

## Development

```
pip install --pre -e ".[test]"
pytest -q tests
```

See the panel's
[docs/pages.md](https://github.com/OpenVoiceOS/ovos-control-panel/blob/dev/docs/pages.md#panel-extensions)
for how an extension is found.

## License

Apache-2.0
