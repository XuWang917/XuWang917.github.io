import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch


spec = importlib.util.spec_from_file_location(
    "stats", Path(__file__).resolve().parents[1] / "scripts/update_publication_stats.py"
)
stats = importlib.util.module_from_spec(spec)
spec.loader.exec_module(stats)

REPOSITORY = "ZJU-OmniAI/Spatial-Interactor"


class GitHubStarsTests(unittest.TestCase):
    def test_reads_stars_not_forks_or_subscribers(self):
        self.assertEqual(stats.extract_stars({
            "full_name": REPOSITORY, "stargazers_count": 89,
            "forks_count": 12, "subscribers_count": 4,
        }, REPOSITORY), 89)

    def test_repository_names_are_case_insensitive(self):
        self.assertEqual(stats.extract_stars({
            "full_name": REPOSITORY.lower(), "stargazers_count": 0,
        }, REPOSITORY), 0)

    def test_invalid_counts_or_wrong_repositories_are_rejected(self):
        for data in [
            {"full_name": "other/Spatial-Interactor", "stargazers_count": 999},
            {"full_name": REPOSITORY, "watchers_count": 89},
            {"full_name": REPOSITORY, "stargazers_count": None},
            {"full_name": REPOSITORY, "stargazers_count": -1},
            {"full_name": REPOSITORY, "stargazers_count": True},
            {"full_name": REPOSITORY, "stargazers_count": "89"},
            [],
        ]:
            with self.subTest(data=data), self.assertRaises(ValueError):
                stats.extract_stars(data, REPOSITORY)

    def test_fetch_uses_repository_endpoint(self):
        with patch.object(stats, "read_json", return_value={
            "full_name": REPOSITORY, "stargazers_count": 89,
        }) as read:
            self.assertEqual(stats.fetch_stars(REPOSITORY), 89)
        read.assert_called_once_with("https://api.github.com/repos/" + REPOSITORY)

    def test_timeout_exhausts_bounded_retries(self):
        with patch.object(stats, "read_json", side_effect=TimeoutError()) as read, patch.object(stats.time, "sleep"):
            with self.assertRaises(TimeoutError):
                stats.fetch_stars(REPOSITORY)
        self.assertEqual(read.call_count, 3)

    def test_failure_retains_newest_published_stars(self):
        saved = {REPOSITORY: {"stargazers_count": 90, "updatedAt": "2026-11-01T00:00:00Z"}}
        published = {REPOSITORY: {"stargazers_count": 89, "updatedAt": "2026-11-02T07:00:00Z"}}
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "stars.json"
            path.write_text(json.dumps(saved), encoding="utf-8")
            with patch.object(stats, "read_json", return_value=published), patch.object(stats, "fetch_stars", side_effect=TimeoutError()):
                result = stats.update_snapshot(
                    path, stats.STARS_PUBLISHED_URL,
                    field="stargazers_count", fetch_metric=stats.fetch_stars,
                )
            self.assertEqual(result, published)
            self.assertEqual(json.loads(path.read_text()), published)

    def test_successful_refresh_can_decrease_stars(self):
        saved = {REPOSITORY: {"stargazers_count": 89, "updatedAt": None}}
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "stars.json"
            path.write_text(json.dumps(saved), encoding="utf-8")
            with patch.object(stats, "read_json", return_value={}), patch.object(stats, "fetch_stars", return_value=88):
                result = stats.update_snapshot(
                    path, stats.STARS_PUBLISHED_URL,
                    field="stargazers_count", fetch_metric=stats.fetch_stars,
                )
            self.assertEqual(result[REPOSITORY]["stargazers_count"], 88)
            self.assertIsNotNone(result[REPOSITORY]["updatedAt"])

    def test_token_is_only_sent_to_https_github_api(self):
        for url in [
            "https://api.github.com/repos/" + REPOSITORY,
            "https://huggingface.co/api/datasets",
            stats.STARS_PUBLISHED_URL,
            "https://api.github.com.invalid/repos/example",
            "http://api.github.com/repos/" + REPOSITORY,
        ]:
            with self.subTest(url=url), patch.dict(stats.os.environ, {"GITHUB_TOKEN": "test-token"}), patch.object(stats, "urlopen") as open_url:
                open_url.return_value.__enter__.return_value = io.StringIO("{}")
                stats.read_json(url)
                request = open_url.call_args.args[0]
                expected = "Bearer test-token" if url.startswith("https://api.github.com/") else None
                self.assertEqual(request.get_header("Authorization"), expected)


if __name__ == "__main__":
    unittest.main()
