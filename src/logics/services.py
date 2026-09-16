"""Access to the personnel directory the bank registers customers from."""

import logging

logger = logging.getLogger(__name__)


def get_people_list_from_web() -> list[dict]:
    """Returns the personnel records the bank is allowed to open accounts for.

    The feed this reads from has not been connected yet, so it hands back an
    empty list: nobody is found, nobody is registered, and the caller reports
    that rather than crashing. Point it at the real directory and the whole
    registration path starts working with no other change.
    """
    logger.warning("personnel directory is not connected, no one can register")
    return []


def find_person(username: str) -> dict | None:
    """Finds the personnel record for a username, or None if there isn't one."""
    person = next(
        (record for record in get_people_list_from_web()
         if record.get("username") == username),
        None,
    )
    if person is None:
        logger.info("no personnel record for %s", username)
    return person
