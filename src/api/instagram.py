"""Provide classes and methods for authenticating and interacting with Instagram."""

import logging
from dataclasses import dataclass
from logging.handlers import RotatingFileHandler
from typing import Optional

from instagrapi import Client  # type: ignore
from instagrapi.exceptions import LoginRequired  # type: ignore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

handler = RotatingFileHandler(
    "mylog.log", maxBytes=10 * 1024 * 1024, backupCount=5
)  # 10 MB files, 5 backups
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

logger.addHandler(handler)


@dataclass
class Instagram:
    """Handles interaction with Instagram through an authenticated client.

    This class provides methods to log in to Instagram using either session
    information or user's credentials, and to get and set the biography
    of the logged-in user's account.

    """

    client: Client = Client()

    def __post_init__(self) -> None:
        """Initialize the Instagram client."""
        self.client.delay_range = [10, 30]

    def login(self, username: str, password: str) -> None:
        """Authenticate with Instagram."""
        try:
            # noinspection PyTypeChecker
            session = self.client.load_settings("session.json")
        except FileNotFoundError as e:
            logger.info(f"Couldn't load session information: {e}")
            session = None
        except Exception as e:
            logger.info(f"Couldn't load session information: {e}")
            session = None

        login_via_session = False
        login_via_credentials = False

        if session:
            try:
                self.client.set_settings(session)
                self.client.login(username=username, password=password)

                try:
                    self.client.get_timeline_feed()
                except LoginRequired:
                    logger.info("Session is invalid, logging in via credentials")
                    old_session = self.client.get_settings()

                    self.client.set_settings({})
                    self.client.set_uuids(old_session["uuids"])

                    self.client.login(username=username, password=password)
                login_via_session = True
            except Exception as e:
                logger.info(f"Couldn't login user using session information: {e}")

        if not login_via_session:
            try:
                logger.info("Attempting to login via credentials")
                if self.client.login(username=username, password=password):
                    # noinspection PyTypeChecker
                    self.client.dump_settings("session.json")
                    login_via_credentials = True
            except Exception as e:
                logger.info(f"Couldn't login user using credentials: {e}")

        if not login_via_session and not login_via_credentials:
            raise Exception("Couldn't login user")

    def get_current_biography(self) -> Optional[str]:
        """Fetch the current biography of the logged-in user."""
        try:
            return self.client.account_info().biography
        except LoginRequired:
            logger.info("Please call login() before calling get_current_biography()")
            return None
        except Exception as e:
            logger.info(f"Couldn't fetch biography: {e}")
            return None

    def set_current_biography(self, biography: str) -> None:
        """Set the current biography of the logged-in user."""
        if not biography:
            raise Exception("Biography cannot be empty")
        if self.get_current_biography() == biography:
            return
        if self.client.account_set_biography(biography):
            logger.info("Biography updated successfully")
        else:
            logger.info("Couldn't update biography")
