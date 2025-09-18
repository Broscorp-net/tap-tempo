"""REST client handling, including TempoStream base class."""

from __future__ import annotations

import decimal
import sys
import typing as t
from urllib.parse import parse_qsl

from singer_sdk.authenticators import BearerTokenAuthenticator
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.pagination import BaseAPIPaginator, BaseHATEOASPaginator  # noqa: TC002
from singer_sdk.streams import RESTStream

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override

if t.TYPE_CHECKING:
    import requests
    from singer_sdk.helpers.types import Context


class TempoPaginator(BaseHATEOASPaginator):
    def get_next_url(self, response):
        return response.json().get("metadata", {}).get("next")


class TempoStream(RESTStream):
    """Tempo stream class."""

    records_jsonpath = "$.results[*]"

    next_page_token_jsonpath = "$.metadata.next"  # noqa: S105

    @override
    def post_process(self, row: dict, context: Context | None = None) -> dict:
        """Inject org_id into every emitted record if provided in config."""
        org_id = self.config.get("org_id")
        if org_id is not None:
            row["org_id"] = org_id
        return row

    @override
    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        return self.config["api_url"]

    @override
    @property
    def authenticator(self) -> BearerTokenAuthenticator:
        """Return a new authenticator object.

        Returns:
            An authenticator instance.
        """
        return BearerTokenAuthenticator.create_for_stream(
            self,
            token=self.config["auth_token"],
        )

    @property
    @override
    def http_headers(self) -> dict:
        """Return the http headers needed.

        Returns:
            A dictionary of HTTP headers.
        """
        headers = {
            "Content-Type": "application/json"
        }
        return headers

    @override
    def get_new_paginator(self) -> BaseAPIPaginator | None:
        """Create a new pagination helper instance.

        If the source API can make use of the `next_page_token_jsonpath`
        attribute, or it contains a `X-Next-Page` header in the response
        then you can remove this method.

        If you need custom pagination that uses page numbers, "next" links, or
        other approaches, please read the guide: https://sdk.meltano.com/en/v0.25.0/guides/pagination-classes.html.

        Returns:
            A pagination helper instance, or ``None`` to indicate pagination
            is not supported.
        """
        return TempoPaginator()

    @override
    def get_url_params(
        self,
        context: Context | None,
        next_page_token: t.Any | None,
    ) -> dict[str, t.Any]:
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary of URL query parameters.
        """

        params: dict = {
            "updatedFrom": self.get_starting_timestamp(context).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "orderBy": "UPDATED",
            "limit": 500,
        }

        if next_page_token:
            params.update(parse_qsl(next_page_token.query))
        return params

    @override
    def parse_response(self, response: requests.Response) -> t.Iterable[dict]:
        """Parse the response and return an iterator of result records.

        Args:
            response: The HTTP ``requests.Response`` object.

        Yields:
            Each record from the source.
        """
        yield from extract_jsonpath(
            self.records_jsonpath,
            input=response.json(parse_float=decimal.Decimal),
        )
