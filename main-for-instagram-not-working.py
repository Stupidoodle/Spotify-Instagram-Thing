import spotify-sus
import time
from instagram_private_api import Client
from common import (
    Client, ClientError, ClientLoginError, ClientCookieExpiredError,
    __version__, to_json, from_json
)
import credentials 
import argparse
import os
import json

creds = credentials.Credentials

USERNAME = creds.spotify_username
CLIENT_ID = creds.spotify_client_id
CLIENT_SECRET = creds.spotify_client_secret
SCOPE = creds.spotify_scope



    

def login_instagram():
    # Example command:
    #   python test_private_api.py -u "xxx" -p "xxx" -settings "saved_auth.json" -save
    parser = argparse.ArgumentParser(description='Test instagram_private_api.py')
    parser.add_argument('-settings', '--settings', dest='settings_file_path', type=str, required=True)
    parser.add_argument('-d', '--device_id', dest='device_id', type=str)
    parser.add_argument('-uu', '--uuid', dest='uuid', type=str)
    parser.add_argument('-save', '--save', action='store_true')
    parser.add_argument('-tests', '--tests', nargs='+')
    parser.add_argument('-debug', '--debug', action='store_true')

    args = parser.parse_args()
    if args.debug:
        logger.setLevel(logging.DEBUG)

    print('Client version: {0!s}'.format(__version__))

    cached_auth = None
    if args.settings_file_path and os.path.isfile(args.settings_file_path):
        with open(args.settings_file_path) as file_data:
            if file_data:
                cached_auth = json.load(file_data, object_hook=from_json)

    # Optional. You can custom the device settings instead of using the default one
    my_custom_device = {
        'phone_manufacturer': 'LGE/lge',
        'phone_model': 'RS988',
        'phone_device': 'h1',
        'android_release': '6.0.1',
        'android_version': 23,
        'phone_dpi': '640dpi',
        'phone_resolution': '1440x2392',
        'phone_chipset': 'h1'
    }

    api = None
    if not cached_auth:

        ts_seed = str(int(os.path.getmtime(__file__)))
        if not args.uuid:
            # Example of how to generate a uuid.
            # You can generate a fixed uuid if you use a fixed value seed
            uuid = Client.generate_uuid(
                seed='{pw!s}.{usr!s}.{ts!s}'.format(**{'pw': creds.instagram_username, 'usr': creds.instagram_password, 'ts': ts_seed}))
        else:
            uuid = args.uuid

        if not args.device_id:
            # Example of how to generate a device id.
            # You can generate a fixed device id if you use a fixed value seed
            device_id = Client.generate_deviceid(
                seed='{usr!s}.{ts!s}.{pw!s}'.format(**{'pw': creds.instagram_password, 'usr': creds.instagram_username, 'ts': ts_seed}))
        else:
            device_id = args.device_id

        # start afresh without existing auth
        try:
            api = Client(
                creds.instagram_username, creds.instagram_password,
                auto_patch=True, drop_incompat_keys=False,
                guid=uuid, device_id=device_id,
                # custom device settings
                **my_custom_device)

        except ClientLoginError:
            print('Login Error. Please check your username and password.')
            sys.exit(99)

        # stuff that you should cache
        cached_auth = api.settings
        if args.save:
            # this auth cache can be re-used for up to 90 days
            with open(args.settings_file_path, 'w') as outfile:
                json.dump(cached_auth, outfile, default=to_json)

    else:
        try:
            # remove previous app version specific info so that we
            # can test the new sig key whenever there's an update
            for k in ['app_version', 'signature_key', 'key_version', 'ig_capabilities']:
                cached_auth.pop(k, None)
            api = Client(
                creds.instagram_username, creds.instagram_password,
                auto_patch=True, drop_incompat_keys=False,
                settings=cached_auth,
                **my_custom_device)

        except ClientCookieExpiredError:
            print('Cookie Expired. Please discard cached auth and login again.')
            sys.exit(99)
    return api

def main():
    api = login_instagram();
    while True:
        playing = spotify.currently_playing()
        if playing:
            song_info = spotify.current_user_playing_track()
            print("Playing: " + song_info["item"]["name"] + " by " + song_info["item"]["artists"][0]["name"])
            print(song_info["item"]["external_urls"]["spotify"])
            results = api.edit_profile("Bryan", "Playing: " + song_info["item"]["name"] + " by " + song_info["item"]["artists"][0]["name"], song_info["item"]["external_urls"]["spotify"], "t4eagario@gmail.com", "+4917682234702", '1')
        else:
            print('Nothing is playing.')
        time.sleep(10)
    

if __name__ == "__main__":
    auth_manager, spotify = create_spotify()
    main()
    
