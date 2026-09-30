#!/usr/bin/env python3
"""Shared jsonschema FormatChecker backed by the Python standard library.

jsonschema does not enforce the ``date-time`` or ``uri`` string formats unless optional
third-party packages (``rfc3339-validator``, ``rfc3987``) are installed. Neither is a
dependency of this harness, so every ``"format": "date-time"`` (44 across schemas/) and the
single ``"format": "uri"`` assertion were silently inert. To enforce them without expanding
the external dependency surface, register standard-library checkers on a shared
``FormatChecker`` and have every validator use it.

The ``date-time`` check accepts the timezone-bearing RFC 3339 shape emitted by the harness,
normalizes a trailing ``Z`` to ``+00:00``, and then uses ``datetime.fromisoformat`` for calendar
and offset validation on the supported Python floor.
"""

from __future__ import annotations

import re
from datetime import datetime
from urllib.parse import urlsplit

from jsonschema import FormatChecker


RFC3339_DATE_TIME_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$"
)


def build_format_checker() -> FormatChecker:
    checker = FormatChecker()

    @checker.checks("date-time", raises=(ValueError, TypeError))
    def _date_time(value: object) -> bool:
        if not isinstance(value, str):
            return True
        if RFC3339_DATE_TIME_RE.fullmatch(value) is None:
            return False
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return parsed.tzinfo is not None and parsed.utcoffset() is not None

    @checker.checks("uri", raises=(ValueError,))
    def _uri(value: object) -> bool:
        if not isinstance(value, str):
            return True
        parts = urlsplit(value)
        return bool(parts.scheme and parts.netloc)

    return checker


# Shared instance; a FormatChecker is effectively read-only after registration.
FORMAT_CHECKER = build_format_checker()
