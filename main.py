"""Main module."""

import logging
import os
import time

from src.api.instagram import Instagram
from src.api.spotify import Spotify

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


RATE_LIMIT_PER_30_SEC = 80
REQUESTS_PER_CYCLE = 2
WAIT_TIME = 30

request_count = 0


def main(spotify: Spotify, instagram: Instagram) -> None:
    """Handle things."""
    current_song = spotify.get_current_song()
    if current_song:
        logger.info(f"Currently listening to: {current_song}")
        instagram.set_current_biography(f"Currently listening to: {current_song}")
    else:
        logger.info("No song is currently playing")
        instagram.set_current_biography("Currently listening to nothing")


if __name__ == "__main__":
    _spotify = Spotify()
    _instagram = Instagram()

    environment = os.getenv("ENV", "dev")
    username = os.getenv("INSTAGRAM_USERNAME", "")
    password = os.getenv("INSTAGRAM_PASSWORD", "")
    scope = "user-read-playback-state"

    if environment == "dev":
        client_id = os.getenv("CLIENT_ID", "")
        client_secret = os.getenv("CLIENT_SECRET", "")
        redirect_uri = os.getenv("REDIRECT_URI", "")
        try:
            _spotify.local_create_spotify(
                client_id=client_id,
                client_secret=client_secret,
                redirect_uri=redirect_uri,
                scope=scope,
            )
            logger.info(
                "Please save the refresh token and set it in your environment variables"
                " server_create_spotify()"
            )
            exit(0)
        except Exception as e:
            logger.error(f"Couldn't login user: {e}")
            exit(1)
    elif environment == "server":
        try:
            _spotify.server_create_spotify(
                scope=scope,
                refresh_token=os.getenv("REFRESH_TOKEN", ""),
            )
            logger.info("Spotify server login successful")
        except Exception as e:
            logger.error(f"Couldn't login user: {e}")
            exit(1)
        try:
            _instagram.login(username=username, password=password)
            logger.info("Instagram login successful")
        except Exception as e:
            logger.error(f"Couldn't login user: {e}")
            exit(1)

        start_time = time.time()

        while True:
            try:
                if request_count + REQUESTS_PER_CYCLE > RATE_LIMIT_PER_30_SEC:
                    elapsed_time = time.time() - start_time
                    if elapsed_time < WAIT_TIME:
                        sleep_time = WAIT_TIME - elapsed_time
                        logger.info(
                            f"Rate limit reached. Sleeping for "
                            f"{sleep_time:.2f} seconds"
                        )
                        time.sleep(sleep_time)
                    request_count = 0
                    start_time = time.time()

                main(_spotify, _instagram)
                request_count += REQUESTS_PER_CYCLE

                time.sleep(0.33)
            except Exception as e:
                logger.error(f"An error occurred: {e}")
                time.sleep(WAIT_TIME)
