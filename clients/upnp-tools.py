#!/usr/bin/env python3
#
# This file is part of upnp-tools, see <https://github.com/MestreLion/upnp>
# Copyright (C) 2022 Rodrigo Silva (MestreLion) <linux@rodrigosilva.com>
# License: GPLv3 or later, at your choice. See <http://www.gnu.org/licenses/gpl>

"""
CLI library demo
"""

import logging
import pathlib
import sys

import upnp


# =============================================================================
def get_external_ip():
    for gateway in upnp.discover(upnp.SEARCH_TARGET.WAN_CONNECTION):
        ip = gateway.actions['GetExternalIPAddres']()[0]
        if ip and not ip == '0.0.0.0':
            return ip
    else:
        raise upnp.UpnpError("No gateway or active internet connection found")


# noinspection PyUnusedLocal
def demo():
    # Just helping static type checkers that can't follow dynamic attributes
    service: upnp.Service
    action: upnp.Action

    st = upnp.SEARCH_TARGET.WAN_CONNECTION  # Enum with handy selectors
    stype: str = st.value  # 'urn:schemas-upnp-org:service:WANIPConnection:1'

    # Discovering Root Devices, filtering by those who offer a given service
    # by themselves or by one of their sub-devices
    for device in upnp.discover(st):
        print(f"{device}\n{device!r}\n")

        # Several ways to select a service in a root device:
        service  = device.services[stype]     # dict Device.services, full type only
        service2 = device[stype]              # shortcut Device dict, by full type
        service3 = device[st]                 # By Enum instance
        service4 = device['WANIPConnection']  # By shorter service type "name"
        service5 = device.WANIPConnection     # Device Attribute, by short name only
        assert service == service2 == service3 == service4 == service5
        print(f"{service}\n{service!r}\n")

        # Several ways to select an action of a service or device:
        action  = service.actions['GetExternalIPAddress']  # dict Service.actions
        action2 = service['GetExternalIPAddress']          # shortcut Service dict
        action3 = service.GetExternalIPAddress             # Service attribute
        action4 = device.actions['GetExternalIPAddress']   # dict Device.actions
        assert action == action2 == action3 == action4
        print(f"{action}\n{action!r}\n")

        # Invoke an action by calling it.
        result = action()
        print(f"{result}\n{result!r}\n")

        # You can use positional and keyword arguments, and even mix them!
        # Keyword arguments will overwrite their corresponding positional ones
        args = tuple(f"pos{i}-{k}" for i, k in enumerate(action.inputs))
        kwargs = {k: f"kw-{k}" for k in action.inputs[1:-1]}

        result = action(*args, **kwargs)
        print(f"{result}\n{result!r}\n")

        # Result is a special collections.namedtuple that allow access by:
        ip = result[0]                       # index, just like any tuple
        ip = result.NewExternalIPAddress     # attribute, like any namedtuple
        ip = result['NewExternalIPAddress']  # key, like a dict! Surprise!

        # Let's be a useful demo...
        if ip and not ip == '0.0.0.0':
            return ip
    else:
        raise upnp.UpnpError("No gateway or active internet connection found")


# =============================================================================
def main():
    loglevel = logging.INFO
    funcs = tuple(k for k, v in globals().items()
                  if callable(v) and k not in ('main',))

    # Lame argparse
    if len(sys.argv) <= 1 or '--help' in sys.argv[1:] or '-h' in sys.argv[1:]:
        print("Usage: {} FUNCTION [ARGS...]\nAvailable functions:\n\t{}".format(
            __file__, "\n\t".join(funcs)))
        return
    if '-v' in sys.argv[1:]:
        loglevel = logging.DEBUG
        sys.argv.remove('-v')
    if '-q' in sys.argv[1:]:
        loglevel = logging.WARNING
        sys.argv.remove('-q')
    logging.basicConfig(level=loglevel, format='%(levelname)-5.5s: %(message)s')

    func = sys.argv[1]
    args = sys.argv[2:]
    if func not in funcs:
        log.error("Function %r does not exist! Try one of:\n\t%s",
                  func, "\n\t".join(funcs))
        return

    def try_int(value):
        try:
            return int(value)
        except ValueError:
            return value
    args = [try_int(_) for _ in args]

    res = globals()[func](*args)
    if res is not None:
        print(res if isinstance(res, str) else repr(res))


log = logging.getLogger(__name__)
if __name__ == '__main__':
    log = logging.getLogger(pathlib.Path(__file__).stem)
    try:
        sys.exit(main())
    except upnp.UpnpError as err:
        log.error(err)
        sys.exit(1)
    except KeyboardInterrupt:
        log.error("Aborted")
