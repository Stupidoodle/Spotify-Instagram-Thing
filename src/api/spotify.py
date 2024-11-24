"""Provide classes and methods for authenticating and interacting with Spotify."""

import logging
from dataclasses import dataclass
from logging.handlers import RotatingFileHandler
from typing import Dict, Optional

import spotipy  # type: ignore
from spotipy.oauth2 import SpotifyOAuth  # type: ignore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

handler = RotatingFileHandler(
    "mylog.log", maxBytes=10 * 1024 * 1024, backupCount=5
)  # 10 MB files, 5 backups
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

logger.addHandler(handler)


@dataclass
class Spotify:
    """Provides methods to authenticate and establish a connection with Spotify.

    The `Spotify` class includes static and instance methods to support local and
    server-based authentication workflows, making it flexible for different
    deployment scenarios.

    Attributes:
    spotify: Optional[spotipy.Spotify]
        An instance of Spotipy's Spotify client,
         initialized after successful authentication.
    spotify_oauth_manager: Optional[SpotifyOAuth]
        An instance of SpotifyOAuth to manage the OAuth authentication process.

    Methods:
    local_create_spotify(client_id, client_secret, redirect_uri, scope):
        Authenticates with Spotify and returns the access and refresh token.
    server_create_spotify(client_id, client_secret, redirect_uri, scope, refresh_token):
        Creates a Spotify server connection using the provided OAuth details.

    """

    spotify: Optional[spotipy.Spotify] = None
    spotify_oauth_manager: Optional[SpotifyOAuth] = None

    def local_create_spotify(
        self, client_id: str, client_secret: str, redirect_uri: str, scope: str
    ) -> Optional[Dict[str, str]]:
        """Authenticate with Spotify and returns the access and refresh token.

        Args:
            client_id: str
                The client ID provided by Spotify for authentication.
            client_secret: str
                The client secret provided by Spotify for authentication.
            redirect_uri: str
                The redirect URI where the response from Spotify will be sent.
            scope: str
                The scope of the access request.

        Returns:
            Dict[str, str]:
                A dictionary containing the access and refresh token.

        """
        if self.spotify:
            return None
        if not self.spotify_oauth_manager:
            self.spotify_oauth_manager = SpotifyOAuth(
                client_id=client_id,
                client_secret=client_secret,
                redirect_uri=redirect_uri,
                scope=scope,
                open_browser=False,
            )

        auth_url = self.spotify_oauth_manager.get_authorize_url()
        logger.info(f"Please go to this URL and authorize access: {auth_url}")

        response_url = input("Paste the full redirect URL here: ")
        code = self.spotify_oauth_manager.parse_response_code(response_url)

        token = self.spotify_oauth_manager.get_access_token(code)
        logger.info(f"Access Token: {token['access_token']}")
        logger.info(f"Refresh Token: {token['refresh_token']}")

        self.spotify = spotipy.Spotify(auth_manager=self.spotify_oauth_manager)

        return token

    def server_create_spotify(
        self,
        scope: str,
        refresh_token: str,
    ) -> None:
        """Create a Spotify server connection using the provided OAuth details.

        Args:
            scope (str): The scope of access requested.
            refresh_token (str): The refresh token to refresh the access token.

        Returns:
            None

        """
        if self.spotify:
            return
        if not self.spotify_oauth_manager:
            self.spotify_oauth_manager = SpotifyOAuth(
                scope=scope,
                open_browser=False,
            )

        self.spotify_oauth_manager.refresh_access_token(refresh_token=refresh_token)
        self.spotify = spotipy.Spotify(auth_manager=self.spotify_oauth_manager)

    def get_current_song(self) -> str:
        """Fetch the current song being played on Spotify.

        Raises:
            Exception: If the Spotify instance is not initialized.

        Returns:
            str: The name of the current song followed by the artist's name.
                 If no song is currently playing, returns an empty string.

        """
        if not self.spotify:
            raise Exception("Spotify not initialized")

        currently_playing = self.spotify.currently_playing()
        if currently_playing:
            if not currently_playing["is_playing"]:
                return ""
            return (
                f"{currently_playing['item']['name']}"
                f" by "
                f"{currently_playing['item']['artists'][0]['name']}"
            )
        else:
            return ""
