import os


from audio2txt.tk_audio import TKAuidoClient
from audio2txt.tk_oss import TKOssClient


class Shared:
    def __init__(self):
        oss_endpoint = os.getenv("TK_OSS_ENDPOINT")
        oss_region = os.getenv("TK_OSS_REGION")
        oss_bucket_name = os.getenv("TK_OSS_BUCKET")
        ak = os.getenv("TK_AK")
        sk = os.getenv("TK_SK")
        tk_oss_client = TKOssClient(ak, sk, oss_endpoint, oss_region, oss_bucket_name)

        appid = os.getenv("TK_APP_ID")
        token = os.getenv("TK_TOKEN")
        cluster = os.getenv("TK_CLUSTER_ID")
        uid = os.getenv("TK_UID")
        tk_audio_client = TKAuidoClient(appid, token, cluster, uid)

        self.tk_oss_client = tk_oss_client
        self.tk_audio_client = tk_audio_client
