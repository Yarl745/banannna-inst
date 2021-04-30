import json

from instagram_private_api import Client
from requests.utils import dict_from_cookiejar

from data.config import IG_USERNAME, IG_PASSWORD

template = {
    "uuids": {
        "phone_id": "5c7ee0b6-d420-4c83-b252-01503e701340",
        "uuid": "4e3eb35e-aa39-39d1-b16d-204a45e4aa73",
        "client_session_id": "cab6e923-e7c9-4993-b979-741536881cc3",
        "advertising_id": "3f0397c6-5505-1123-ba15-5dd3a8acce06",
        "device_id": "android-3f8a1301e66b623e"
    },
    "cookie": {
        "csrftoken": "ZLsFNa04RqA06BzRKzx60dqLDLCYVfTq",
        "ds_user": "banannnabot",
        "ds_user_id": "46287123664",
        "ig_did": "xxx",
        "ig_direct_region_hint": "FRC",
        "igfl": "banannnabot",
        "is_starred_enabled": "yes",
        "mid": "YIgsPgABAAEBcIZEYYSXG3M4VhBC",
        "rur": "PRN",
        "sessionid": "46287123664%3ApGUZnuJCcfD4IH%3A5",
        "shbid": "xxx",
        "shbts": "xxx",
        "urlgen": "xxx"
    },
    "timing_value": {
        "last_login": 1619653185.8064287,
        "last_experiments": 1619653256.2109787
    },
    "device_settings": {
        "app_version": "117.0.0.28.123",
        "android_version": "28",
        "android_release": "9.0",
        "dpi": "420dpi",
        "resolution": "1080x1920",
        "manufacturer": "Huawei",
        "device": "Mate 10 Pro",
        "model": "Mate 10 Pro",
        "cpu": "qcom",
        "version_code": "180322800"
    },
    "user_agent": "Instagram 117.0.0.28.123 Android (28/9.0; 420dpi; 1080x1920; Huawei; HUAWEI MATE 10 PRO; Mate10Pro; qcom; de_DE; 180322800)"
}


def get_cookie() -> dict:
    api = Client(
        username=IG_USERNAME,
        password=IG_PASSWORD,
        auto_patch=True
    )
    cookie = dict_from_cookiejar(api.cookie_jar)
    cookie.update(
        ds_user=IG_USERNAME,
        igfl=IG_USERNAME
    )
    return cookie


def update_cookie():
    new_cookie = get_cookie()
    template["cookie"].update(new_cookie)
    with open('config/banannnabot_uuid_and_cookie.json', 'w') as file:
        json.dump(template, file)

