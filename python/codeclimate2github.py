#!/usr/bin/env python3
import json
import logging
from argparse import ArgumentParser, FileType, Namespace
from collections import defaultdict
from sys import exit

from github import Github

LOGGER = logging.getLogger(__file__)
LOGGER.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
LOGGER.addHandler(ch)


def args() -> Namespace:
    parser = ArgumentParser(
        description="Adds detected defections in Code climate format to Github reviews in a form of comments"
    )
    parser.add_argument("--url", help="GitHub API base URL", required=True, type=str)
    parser.add_argument(
        "-token", help="Authentication token (GitHub personal access token or username/password)", required=True, type=str
    )
    parser.add_argument("--project-id", help="GitHub repository full name or ID", required=True, type=str)
    parser.add_argument("--pull-request-id", help="Pull request number", required=True, type=int)
    parser.add_argument(
        "--input",
        help="File with Code Climate report",
        required=True,
        type=FileType("r"),
        default="-",
    )

    return parser.parse_args()


def main():
    cmd = args()
    data = json.load(cmd.input)
    publish_comments(data, cmd.url, cmd.token, cmd.project_id, cmd.pull_request_id)


def get_diff_discussions(pr):
    diff_discussions = defaultdict(set)

    for discussion in pr.get_issue_comments():
        if discussion.diff_hunk:
            path = discussion.path
            line = discussion.position
            diff_discussions[f"{path}:{line}"].add(discussion.body)
    return diff_discussions


def create_comment_payload(defect, last_diff):
    fingerprint = defect["fingerprint"]
    rule = defect["check_name"]
    desc = defect["description"]
    path = defect["location"]["path"]
    line = defect["location"]["positions"]["begin"]["line"]
    body = f"{fingerprint}: {rule}\n\n{desc}"

    return {
        "body": body,
        "path": path,
        "position": line,
        "commit_id": last_diff.sha,
    }


def publish_comments(defects, github_base_url, token, proj_id, pr_number):
    gh = Github(base_url=github_base_url, login_or_token=token)

    repo = gh.get_repo(full_name_or_id=proj_id)
    pr = repo.get_pull(pr_number)
    diff_discussions = get_diff_discussions(pr)

    last_diff = pr.get_files()[-1]

    for defect in defects:
        payload = create_comment_payload(defect, last_diff)
        path = payload["path"]
        line = payload["position"]

        if any(
                comment.body == payload["body"] and comment.path == path and comment.position == line
                for comment in diff_discussions
        ):
            LOGGER.debug(
                "Skipping already reported defects %s at file %s:%s",
                defect["check_name"],
                path,
                line
            )
            continue

        # Use create_issue_comment to create regular comments
        comment = pr.create_issue_comment(
            body=payload["body"]
        )

        LOGGER.debug("Created issue comment %s", comment)

    exit(int(len(defects) != 0))


if __name__ == '__main__':
    main()
