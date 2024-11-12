import tos
from tos import HttpMethodType

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tos.models2 import ListObjectType2Output


class TKOssClient:
    def __init__(self, ak, sk, endpoint, region, bucket_name):
        # ak, sk, endpoint, region
        self.ak = ak
        self.sk = sk
        self.endpoint = endpoint
        self.region = region
        self.bucket_name = bucket_name
        self.client = tos.TosClientV2(ak, sk, endpoint, region)

    def pre_signed_url(self, object_key) -> str:
        pre_signed_url_output = self.client.pre_signed_url(HttpMethodType.Http_Method_Get, self.bucket_name, object_key)
        return pre_signed_url_output.signed_url

    def put_object(self, object_key: str, content: bytes) -> bool:
        result = self.client.put_object(self.bucket_name, object_key, content=content)
        if result.status_code == 200:
            return True
        else:
            return False

    def list_objects_type2(self, prefix: str, max_keys: int = 1000) -> "ListObjectType2Output":
        result = self.client.list_objects_type2(self.bucket_name, prefix=prefix, max_keys=max_keys)
        return result

    def exists_object(self, object_key: str) -> bool:
        try:
            result = self.client.head_object(self.bucket_name, object_key)
            return result.status_code == 200
        except tos.exceptions.TosServerError as e:
            return False
