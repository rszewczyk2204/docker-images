#!/usr/bin/env python3
import logging
import subprocess
from argparse import ArgumentParser, Namespace
from os.path import splitext
from pathlib import Path

from github import Github

LOGGER = logging.getLogger(__file__)
LOGGER.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
LOGGER.addHandler(ch)

SUPPORTED_LABELS = {"api", "ci"}

def args() -> Namespace:
    parser = ArgumentParser(
        description="Bot to automate different jobs on github"
    )
    parser.add_argument("--url", help="Github API address", required=True, type=str)
    parser.add_argument("--base-sha", help="Base revision", required=True, type=str)
    parser.add_argument(
        "--token", help="Authentication token", required=True, type=str
    )
    parser.add_argument(
        "--project-name", help="Full project name", required=True, type=str
    )
    parser.add_argument(
        "--pull-request-number",
        help="Unique in whole project",
        required=True,
        type=int,
    )
    return parser.parse_args()


def main():
    cmd = args()
    labels = detected_labels(cmd.base_sha)
    update_labels(labels, cmd.url, cmd.token, cmd.project_id, cmd.pull_request_id)


def detected_labels(base_sha: str) -> set[str]:
    resp = subprocess.run(
        ['git', 'diff', '--name-only', base_sha + '..'],
        check=True,
        stdout=subprocess.PIPE
    )
    files = set(resp.stdout.decode("utf8").rstrip().split("\n"))
    api_files = [file for file in files if file.endswith(".openapi.yml")]
    extensions = {splitext(file)[1] for file in files}
    labels = set()
    for api_file in api_files:
        path = Path(api_file)
        label = "api:" + path.name.partition(".")[0]
        labels.add(label)
    if labels:
        labels.add("api")
    if ".gitlab-ci.yml" in files:
        labels.add("ci")
    if ".sql" in files:
        labels.add("sql")
    if ".java" in extensions:
        labels.add("java")
    if ".py" in extensions:
        labels.add("python")
    return labels


def update_labels(
        labels: set[str], github_url: str, token: str, project_name: str, pr_number: int
):
    gh = Github(base_url=github_url, login_or_token=token)

    pr = gh.get_repo(full_name_or_id=project_name).get_pull(pr_number)
    old_labels = set(pr.labels)
    for pr_label in pr.labels:
        if pr_label.name.startswith("api:") or pr_label.name in SUPPORTED_LABELS:
            continue
        labels.add(pr_label.name)
    if old_labels == labels:
        LOGGER.debug("No need to update labels %s", labels)
    for label in labels:
        pr.add_to_labels(label)


if __name__ == "__main__":
    main()