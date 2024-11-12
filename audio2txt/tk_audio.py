import json
import logging
from dotenv import load_dotenv
import os

import requests

load_dotenv()


class UploadAuth(requests.auth.AuthBase):
    def __init__(self, appid, token, cluster, uid):
        self.conf = (appid, token, cluster, uid)

    def __call__(self, r):
        appid, token, cluster, uid = self.conf
        r.headers["Authorization"] = f"Bearer; {token}"
        r.headers["Content-Type"] = "application/json"
        body_data = json.loads(r.body)
        body_data.update({"app": {"appid": appid, "token": token, "cluster": cluster}})
        body_data.update({"user": {"uid": uid}})
        r.body = json.dumps(body_data)
        print(f"UploadAuth: {r.body}, {r.url}, {r.headers}")
        return r


class QueryAuth(requests.auth.AuthBase):
    def __init__(self, appid, token, cluster, uid):
        self.conf = (appid, token, cluster, uid)

    def __call__(self, r):
        appid, token, cluster, uid = self.conf
        r.headers["Authorization"] = f"Bearer; {token}"
        r.headers["Content-Type"] = "application/json"
        body_data = json.loads(r.body)
        body_data.update({"appid": appid, "token": token, "cluster": cluster})
        r.body = json.dumps(body_data)
        print(f"QueryAuth: {r.body}, {r.url}, {r.headers}")
        return r


class TKAuidoClient:
    def __init__(self, appid, token, cluster, uid):
        self.conf = (appid, token, cluster, uid)

    def upload_audio(self, audio_url):
        url = "https://openspeech.bytedance.com/api/v1/auc/submit"
        body = {
            "audio": {"format": "mp3", "url": audio_url},
            "additions": {"use_itn": "False", "with_speaker_info": "True"},
        }
        appid, token, cluster, uid = self.conf
        upload_auth = UploadAuth(appid, token, cluster, uid)
        res = requests.post(url, json=body, auth=upload_auth)
        res_data = res.json()
        logging.info(f"upload_audio: {res_data}")
        return res_data

    def query_audio_result(self, id):
        url = "https://openspeech.bytedance.com/api/v1/auc/query"
        body = {"id": id}
        appid, token, cluster, uid = self.conf
        query_auth = QueryAuth(appid, token, cluster, uid)
        res = requests.post(url, json=body, auth=query_auth)
        res_data = res.json()
        logging.info(f"query_audio_result: {res_data}")
        return res_data
