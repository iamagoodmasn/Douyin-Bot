#-*- coding: UTF-8 -*-
import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.iai.v20200303 import iai_client, models
import base64
import time
url_preffix="iai.tencentcloudapi.com"


def setParams(array, key, value):
    array[key] = value


class AiPlat(object):
    def __init__(self, app_id, app_key):
        self.app_id = app_id
        self.app_key = app_key
        self.data = {}

    def invoke(self, data):
        cred = credential.Credential(self.app_id,self.app_key)
        httpProfile = HttpProfile()
        httpProfile.endpoint = url_preffix
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = iai_client.IaiClient(cred, "ap-beijing", clientProfile)
        req = models.DetectFaceRequest()
        params = data
        try:
            req.from_json_string(json.dumps(params))
            resp = client.DetectFace(req)
            dict_rsp = json.loads(resp.to_json_string())
            dict_rsp.update({'ret': 0})
            return dict_rsp
        except Exception as e:
            print(e)
            return {'ret': -1}

    def face_detectface(self, image):
        image_data = base64.b64encode(image)
        #print(image_data)
        #time.sleep(5)
        setParams(self.data, 'Image', image_data.decode('utf-8'))
        setParams(self.data, "NeedFaceAttributes", 1)
        setParams(self.data, "FaceModelVersion", "3.0")
        return self.invoke(self.data)

