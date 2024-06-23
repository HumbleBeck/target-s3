"""target-s3 target sink class, which handles writing streams."""

from __future__ import annotations

from singer_sdk.sinks import BatchSink
from smart_open import open
from datetime import datetime
import uuid
import json


class TargetS3Sink(BatchSink):
    """target-s3 target sink class."""

    @property
    def max_size(self):
        return self.config.get("max_records", 100000)

    def get_url(self):
        bucket_name: str = self.config.get("bucket_name")
        prefix: str = self.config.get("prefix", "meltano")

        today = datetime.today()

        return "s3://{}.jsonl".format(
            "/".join([bucket_name, prefix, self.stream_name, f"date={today.strftime('%Y-%m-%d')}", str(uuid.uuid4())])
        )

    def process_batch(self, context: dict) -> None:
        """Write out any prepped records and return once fully written.

        Args:
            context: Stream partition or context dictionary.
        """
        # Sample:
        # ------
        # client.upload(context["file_path"])  # Upload file
        # Path(context["file_path"]).unlink()  # Delete local copy

        records = context["records"]
        data = "\n".join([json.dumps(record, default=str) for record in records])
        with open(
            self.get_url(),
            "wb"
        ) as fout:
            fout.write(str.encode(data))
