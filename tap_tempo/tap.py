"""Tempo tap class."""

from __future__ import annotations

import sys

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

from tap_tempo import streams

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override


class TapTempo(Tap):
    """Tempo tap class."""

    name = "tap-tempo"

    # TODO: Update this section with the actual config values you expect:
    config_jsonschema = th.PropertiesList(
        th.Property(
            "auth_token",
            th.StringType(nullable=False),
            required=True,
            secret=True,  # Flag config as protected.
            title="Auth Token",
            description="The token to authenticate against the API service",
        ),
        th.Property(
            "start_date",
            th.DateTimeType(nullable=True),
            description="The earliest record date to sync",
        ),
        th.Property(
            "api_url",
            th.StringType(nullable=False),
            title="API URL",
            default="https://api.tempo.io/4",
            description="The url for the API service",
        ),
        th.Property(
            "user_agent",
            th.StringType(nullable=True),
            description=(
                "A custom User-Agent header to send with each request. Default is "
                "'<tap_name>/<tap_version>'"
            ),
        ),
        th.Property(
            "org_id",
            th.StringType(nullable=True),
            description="Organization id to stamp into each record.",
        ),
    ).to_dict()

    @override
    def discover_streams(self) -> list[streams.TempoStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            streams.WorklogsStream(self)
        ]


if __name__ == "__main__":
    TapTempo.cli()
