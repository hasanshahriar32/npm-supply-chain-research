#!/usr/bin/env python3
"""Conservative repository parsing and public workflow observation semantics."""
from urllib.parse import unquote, urlsplit
import re


def parse_github_repository(value):
    """Return a canonical owner/repository, preserving dots in repository names.

    This is lexical normalization, not remote verification or a redirect lookup.
    Only explicit GitHub hosts/shorthands are accepted.
    """
    if isinstance(value, dict):
        value = value.get("url")
    if not isinstance(value, str) or not value.strip():
        return None, None
    value = value.strip()
    if value.startswith("git+"):
        value = value[4:]
    if value.startswith("github:"):
        value = "https://github.com/" + value[len("github:"):]
    elif value.startswith("git@github.com:"):
        value = "ssh://git@github.com/" + value[len("git@github.com:"):]
    elif value.startswith("github.com:"):
        value = "https://github.com/" + value[len("github.com:"):]
    try:
        parsed = urlsplit(value)
        if parsed.scheme not in {"https", "http", "ssh", "git"} or (parsed.hostname or "").casefold() not in {"github.com", "www.github.com"}:
            return None, None
    except ValueError:
        return None, None
    pieces = parsed.path.strip("/").split("/")
    if len(pieces) < 2:
        return None, None
    owner, repository = (unquote(pieces[0]), unquote(pieces[1]))
    if repository.endswith(".git"):
        repository = repository[:-4]
    if not all(re.fullmatch(r"[A-Za-z0-9_.-]+", part or "") and part not in {".", ".."} for part in (owner, repository)):
        return None, None
    return owner.casefold(), repository.casefold()


def classify_workflow_response(http_status, payload):
    """Keep unavailable/error states separate from an observed missing directory.

    Return (state, directory_flag, detail). A positive flag is directory presence,
    not evidence of execution, token scope, or security-control adoption.
    """
    if http_status in {401, 403, 404}:
        return "unavailable", None, "http_access_or_not_found"
    if http_status != 200:
        return "request_error", None, "http_error"
    if not isinstance(payload, dict) or payload.get("errors"):
        return "request_error", None, "graphql_errors_or_invalid_payload"
    data = payload.get("data")
    if not isinstance(data, dict) or "repository" not in data:
        return "request_error", None, "missing_repository_result"
    repository = data["repository"]
    if repository is None:
        return "unavailable", None, "repository_not_visible"
    if not isinstance(repository, dict) or "object" not in repository:
        return "request_error", None, "missing_object_result"
    obj = repository["object"]
    if obj is None:
        return "directory_not_observed", 0, "visible_repository_head_directory_not_returned"
    if isinstance(obj, dict) and obj.get("__typename") == "Tree" and isinstance(obj.get("entries"), list):
        return "directory_observed", 1, "public_head_directory_tree"
    return "request_error", None, "unexpected_object_shape"
