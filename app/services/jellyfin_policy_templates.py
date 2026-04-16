import logging
import re

from app.extensions import db
from app.models import JellyfinPolicyTemplate

_TAG_RE = re.compile(r"^[\w\-+. ]+$")


def parse_tags(raw: str | None) -> list[str]:
    if not raw:
        return []
    values = []
    for tag in raw.split(","):
        normalized = tag.strip()
        if not normalized:
            continue
        values.append(normalized)
    # De-duplicate while preserving order
    deduped = []
    seen = set()
    for item in values:
        key = item.lower()
        if key in seen:
            continue
        seen.add(key)
        deduped.append(item)
    return deduped


def validate_tags(tags: list[str]) -> list[str]:
    errors: list[str] = []
    for tag in tags:
        if len(tag) > 64:
            errors.append(f"Tag '{tag}' is too long (max 64 characters).")
            continue
        if not _TAG_RE.fullmatch(tag):
            errors.append(
                f"Tag '{tag}' contains invalid characters. Use letters, numbers, spaces, -, _, + or ."
            )
    return errors


def create_template(name: str, allowed_tags: list[str], blocked_tags: list[str]) -> None:
    template = JellyfinPolicyTemplate(name=name.strip())
    template.set_allowed_tags(allowed_tags)
    template.set_blocked_tags(blocked_tags)
    db.session.add(template)
    db.session.commit()


def update_template(
    template: JellyfinPolicyTemplate,
    name: str,
    allowed_tags: list[str],
    blocked_tags: list[str],
) -> None:
    template.name = name.strip()
    template.set_allowed_tags(allowed_tags)
    template.set_blocked_tags(blocked_tags)
    db.session.commit()


def apply_template_to_policy(
    policy: dict,
    template: JellyfinPolicyTemplate,
) -> dict:
    allowed_tags = template.get_allowed_tags()
    blocked_tags = template.get_blocked_tags()

    policy["AllowedTags"] = allowed_tags
    policy["BlockedTags"] = blocked_tags

    return policy


def log_policy_template_failure(code: str, username: str, message: str) -> None:
    logging.error(
        "Jellyfin policy template apply failed (invite=%s user=%s): %s",
        code,
        username,
        message,
    )
