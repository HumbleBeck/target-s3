"""target-s3 target class."""

from __future__ import annotations

from singer_sdk import typing as th
from singer_sdk.target_base import Target

from target_s3.sinks import TargetS3Sink


class TargetS3(Target):
    """Sample target for target-s3."""

    name = "target-s3"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "bucket_name",
            th.StringType,
            required=True,
            description="S3 bucket name to the target output file",
        ),
        th.Property(
            "prefix",
            th.StringType,
            description="S3 prefix to the target output file",
        ),
        th.Property(
            "max_records",
            th.NumberType,
            description="The maximum number of records to batch",
        ),
    ).to_dict()

    default_sink_class = TargetS3Sink


if __name__ == "__main__":
    TargetS3.cli()
