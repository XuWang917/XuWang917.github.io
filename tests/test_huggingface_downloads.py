import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from urllib.parse import parse_qs, urlsplit


spec = importlib.util.spec_from_file_location(
    "downloads", Path(__file__).resolve().parents[1] / "scripts/update_publication_stats.py"
)
downloads = importlib.util.module_from_spec(spec)
spec.loader.exec_module(downloads)

DATASET = "kagakouko/LSI-108K"
SECOND = "wx91726/SpatialGen-Bench"


class DownloadStatisticsTests(unittest.TestCase):
    def test_uses_exact_dataset_and_all_time_count(self):
        self.assertEqual(downloads.extract_downloads([
            {"id": "other/LSI-108K", "downloadsAllTime": 9999},
            {"id": DATASET, "downloads": 50, "downloadsAllTime": 1577},
        ], DATASET), 1577)

    def test_never_substitutes_monthly_or_invalid_values(self):
        for entry in [
            {"downloads": 100}, {"downloadsAllTime": None},
            {"downloadsAllTime": -1}, {"downloadsAllTime": True},
            {"downloadsAllTime": "1577"},
        ]:
            with self.subTest(entry=entry), self.assertRaises(ValueError):
                downloads.extract_downloads([dict(entry, id=DATASET)], DATASET)

    def test_zero_is_valid(self):
        self.assertEqual(downloads.extract_downloads([{"id": DATASET, "downloadsAllTime": 0}], DATASET), 0)

    def test_request_expands_cumulative_statistics(self):
        with patch.object(downloads, "read_json", return_value=[{"id": DATASET, "downloadsAllTime": 42}]) as read:
            self.assertEqual(downloads.fetch_downloads(DATASET), 42)
        query = parse_qs(urlsplit(read.call_args.args[0]).query)
        self.assertEqual(query, {"author": ["kagakouko"], "search": ["LSI-108K"], "expand[]": ["downloadsAllTime"]})

    def test_timeout_is_retried(self):
        with patch.object(downloads, "read_json", side_effect=[TimeoutError(), [{"id": DATASET, "downloadsAllTime": 42}]]), patch.object(downloads.time, "sleep") as sleep:
            self.assertEqual(downloads.fetch_downloads(DATASET), 42)
            sleep.assert_called_once_with(1)

    def test_failure_retains_newest_published_value(self):
        saved = {DATASET: {"downloadsAllTime": 10, "updatedAt": None}}
        published = {DATASET: {"downloadsAllTime": 80, "updatedAt": "2026-11-01T00:00:00Z"}}
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "downloads.json"
            path.write_text(json.dumps(saved), encoding="utf-8")
            with patch.object(downloads, "read_json", return_value=published), patch.object(downloads, "fetch_downloads", side_effect=TimeoutError()):
                result = downloads.update_snapshot(path)
            self.assertEqual(result, published)
            self.assertEqual(json.loads(path.read_text()), published)

    def test_one_dataset_failure_does_not_block_another(self):
        saved = {key: {"downloadsAllTime": 10, "updatedAt": None} for key in [DATASET, SECOND]}
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "downloads.json"
            path.write_text(json.dumps(saved), encoding="utf-8")
            with patch.object(downloads, "read_json", side_effect=TimeoutError()), patch.object(downloads, "fetch_downloads", side_effect=[TimeoutError(), 2345]):
                result = downloads.update_snapshot(path)
            self.assertEqual(result[DATASET], saved[DATASET])
            self.assertEqual(result[SECOND]["downloadsAllTime"], 2345)
            self.assertIsNotNone(result[SECOND]["updatedAt"])

    def test_older_or_invalid_published_data_is_not_used(self):
        snapshot = {DATASET: {"downloadsAllTime": 80, "updatedAt": "2026-11-01T00:00:00Z"}}
        for published in [
            {DATASET: {"downloadsAllTime": 10, "updatedAt": "2026-10-01T00:00:00Z"}},
            {DATASET: {"downloadsAllTime": None, "updatedAt": "2026-11-02T00:00:00Z"}},
            [],
        ]:
            result = copy.deepcopy(snapshot)
            downloads.merge_published(result, published)
            self.assertEqual(result, snapshot)


if __name__ == "__main__":
    unittest.main()
