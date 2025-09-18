"""Tests standard tap features using the built-in SDK tests library."""

import datetime
import os

from singer_sdk.testing import get_tap_test_class

from tap_tempo.tap import TapTempo

SAMPLE_CONFIG = {
    "start_date": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d"),
    "api_url": "https://api.tempo.io/4",
    "auth_token": os.environ.get("TAP_TEMPO_AUTH_TOKEN"),
}


# Run standard built-in tap tests from the SDK:
TestTapTempo = get_tap_test_class(
    tap_class=TapTempo,
    config=SAMPLE_CONFIG,
)
