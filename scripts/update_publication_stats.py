from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys
import time
from urllib.parse import quote, urlencode, urlsplit
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
PUBLISHED_URL = "https://xuwang917.github.io/assets/data/huggingface-downloads.json"
STARS_PUBLISHED_URL = "https://xuwang917.github.io/assets/data/github-stars.json"


def read_json(url, timeout=15):
    headers = {
        "Accept": "application/json",
        "User-Agent": "XuWang917-homepage-publication-stats",
    }
    parsed = urlsplit(url)
    if parsed.scheme == "https" and parsed.netloc == "api.github.com":
        headers["Accept"] = "application/vnd.github+json"
        token = os.environ.get("GITHUB_TOKEN")
        if token:
            headers["Authorization"] = "Bearer " + token
    request = Request(url, headers=headers)
    with urlopen(request, timeout=timeout) as response:
        return json.load(response)


def valid_count(value):
    return type(value) is int and value >= 0


def checked_at(entry):
    try:
        return datetime.fromisoformat(entry["updatedAt"].replace("Z", "+00:00")).astimezone(timezone.utc)
    except (KeyError, TypeError, AttributeError, ValueError):
        return datetime.min.replace(tzinfo=timezone.utc)


def merge_published(snapshot, published, field="downloadsAllTime"):
    if not isinstance(published, dict):
        return
    for identifier, current in snapshot.items():
        entry = published.get(identifier)
        if (
            isinstance(entry, dict)
            and valid_count(entry.get(field))
            and checked_at(entry) > checked_at(current)
        ):
            snapshot[identifier] = {
                field: entry[field],
                "updatedAt": entry["updatedAt"],
            }


def extract_downloads(data, dataset):
    if isinstance(data, list):
        for entry in data:
            if not isinstance(entry, dict) or entry.get("id") != dataset:
                continue
            count = entry.get("downloadsAllTime")
            if valid_count(count):
                return count
    raise ValueError("Missing valid cumulative downloads for " + dataset)


def extract_stars(data, repository):
    if (
        isinstance(data, dict)
        and isinstance(data.get("full_name"), str)
        and data["full_name"].casefold() == repository.casefold()
        and valid_count(data.get("stargazers_count"))
    ):
        return data["stargazers_count"]
    raise ValueError("Missing valid GitHub stars for " + repository)


def fetch_count(url, identifier, extract_count):
    for attempt in range(3):
        try:
            return extract_count(read_json(url), identifier)
        except (OSError, ValueError) as error:
            if attempt == 2:
                raise
            print("Retrying {}: {}".format(identifier, error), file=sys.stderr)
            time.sleep(2 ** attempt)


def fetch_downloads(dataset):
    author, name = dataset.split("/", 1)
    query = urlencode({"author": author, "search": name, "expand[]": "downloadsAllTime"})
    return fetch_count("https://huggingface.co/api/datasets?" + query, dataset, extract_downloads)


def fetch_stars(repository):
    encoded = "/".join(quote(part, safe="") for part in repository.split("/"))
    return fetch_count("https://api.github.com/repos/" + encoded, repository, extract_stars)


def update_snapshot(path, published_url=PUBLISHED_URL, field="downloadsAllTime", fetch_metric=None):
    if fetch_metric is None:
        fetch_metric = fetch_downloads
    snapshot = json.loads(path.read_text(encoding="utf-8"))
    for identifier, entry in snapshot.items():
        if not isinstance(entry, dict) or not valid_count(entry.get(field)):
            raise ValueError("Invalid saved statistics for " + identifier)

    # Recover the last deployment before refreshing, since scheduled builds do not commit data.
    try:
        merge_published(snapshot, read_json(published_url, timeout=10), field)
    except (OSError, ValueError) as error:
        print("Published snapshot unavailable: " + str(error), file=sys.stderr)

    for identifier in snapshot:
        try:
            count = fetch_metric(identifier)
        except (OSError, ValueError) as error:
            print("Keeping last successful statistics for {}: {}".format(identifier, error), file=sys.stderr)
            continue
        snapshot[identifier] = {
            field: count,
            "updatedAt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        }
        print("{}: {} {}".format(identifier, count, field))

    path.write_text(json.dumps(snapshot, indent=2) + "\n", encoding="utf-8")
    return snapshot


if __name__ == "__main__":
    update_snapshot(ROOT / "_data/huggingface_downloads.json")
    update_snapshot(
        ROOT / "_data/github_stars.json", STARS_PUBLISHED_URL,
        field="stargazers_count", fetch_metric=fetch_stars,
    )
