"""Stream type classes for tap-tempo."""

from __future__ import annotations

import typing as t

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_tempo.client import TempoStream


class WorklogsStream(TempoStream):
    """Tempo worklogs stream."""

    name = "worklogs"
    path = "/worklogs"
    primary_keys: t.ClassVar[list[str]] = ["tempoWorklogId"]
    replication_key = "updatedAt"
    replication_method = "INCREMENTAL"

    schema = th.PropertiesList(
        th.Property("description", th.StringType),
        th.Property(
            "tempoWorklogId",
            th.IntegerType,
            description="Tempo worklog ID",
            required=True,
        ),
        th.Property(
            "attributes",
            th.ObjectType(th.Property("self", th.StringType), th.Property("values", th.ArrayType(
                th.ObjectType(th.Property("key", th.StringType), th.Property("value", th.AnyType))))),
            description="The user's age in years",
        ),
        th.Property(
            "author",
            th.ObjectType(th.Property("self", th.StringType), th.Property("accountId", th.StringType)),
        ),
        th.Property(
            "issue",
            th.ObjectType(th.Property("self", th.StringType), th.Property("id", th.IntegerType)),
        ),
        th.Property("billableSeconds", th.IntegerType),
        th.Property("createdAt", th.DateTimeType),
        th.Property(
            "self",
            th.StringType,
            required=True,
        ),
        th.Property("startDate", th.DateType),
        th.Property("startDateTimeUtc", th.DateTimeType),
        th.Property("updatedAt", th.DateTimeType),
        th.Property("timeSpentSeconds", th.IntegerType),
    ).to_dict()
