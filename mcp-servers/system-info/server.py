from __future__ import annotations

import getpass
import os
import platform
import shutil
import socket
import time
from typing import Any, Dict, Optional

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("local-system-info")

_SAFE_ENV_KEYS = ("TZ", "LANG", "LC_ALL", "USER", "HOME", "SHELL", "TERM")


def _safe_sysconf(name: str) -> Optional[int]:
    try:
        return os.sysconf(name)
    except (AttributeError, ValueError, OSError):
        return None


def _get_memory_info() -> Dict[str, Optional[int]]:
    page_size = _safe_sysconf("SC_PAGE_SIZE")
    phys_pages = _safe_sysconf("SC_PHYS_PAGES")
    avail_pages = _safe_sysconf("SC_AVPHYS_PAGES")

    total_bytes = None
    available_bytes = None

    if page_size and phys_pages:
        total_bytes = page_size * phys_pages
    if page_size and avail_pages:
        available_bytes = page_size * avail_pages

    return {
        "total_bytes": total_bytes,
        "available_bytes": available_bytes,
        "page_size_bytes": page_size,
    }


def _get_load_average() -> Optional[Dict[str, float]]:
    try:
        load_1, load_5, load_15 = os.getloadavg()
    except (AttributeError, OSError):
        return None
    return {"1m": load_1, "5m": load_5, "15m": load_15}


def _get_uptime_seconds() -> Optional[float]:
    try:
        with open("/proc/uptime", "r", encoding="utf-8") as handle:
            value = handle.read().strip().split()[0]
        return float(value)
    except (FileNotFoundError, ValueError, OSError):
        return None


def _get_safe_env() -> Dict[str, str]:
    return {key: value for key, value in os.environ.items() if key in _SAFE_ENV_KEYS}


@mcp.tool()
def get_system_info(include_env: bool = False) -> Dict[str, Any]:
    """Return basic system configuration for the current runtime."""
    disk = shutil.disk_usage("/")

    info: Dict[str, Any] = {
        "hostname": socket.gethostname(),
        "fqdn": socket.getfqdn(),
        "user": getpass.getuser(),
        "python_version": platform.python_version(),
        "os": {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "platform": platform.platform(),
        },
        "runtime": {
            "pid": os.getpid(),
            "cwd": os.getcwd(),
            "cpu_count": os.cpu_count(),
            "load_average": _get_load_average(),
            "uptime_seconds": _get_uptime_seconds(),
            "timezone": {
                "tzname": time.tzname,
                "offset_seconds": -time.timezone,
            },
        },
        "memory": _get_memory_info(),
        "disk": {
            "root_total_bytes": disk.total,
            "root_used_bytes": disk.used,
            "root_free_bytes": disk.free,
        },
    }

    if include_env:
        info["env"] = _get_safe_env()

    return info


if __name__ == "__main__":
    mcp.run()
