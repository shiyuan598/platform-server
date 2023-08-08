# 参考：腾讯云短信服务SDK
# https://cloud.tencent.com/document/product/382
# 腾讯云账户管理
# https://console.cloud.tencent.com/smsv2

import json
from datetime import datetime
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.sms.v20210111 import sms_client, models
from config.setting import SMS_ENABLE

secretId = "AKIDtc5JI2YrvjKL6bsteARUIveHhspwrXyB"
secretKey = "BBzZeFckcYP1ObaKp45qLcdQzNWQ5Vhd"

def sendMessage(SmsSdkAppId = "1400814469", SignName = "ZHITO小程序", TemplateId="", TemplateParamSet=[], PhoneNumberSet=[]):
    try:
        if SMS_ENABLE == False:
            return
        # 实例化一个认证对象，入参需要传入腾讯云账户 SecretId 和 SecretKey，此处还需注意密钥对的保密
        # 代码泄露可能会导致 SecretId 和 SecretKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考，建议采用更安全的方式来使用密钥，请参见：https://cloud.tencent.com/document/product/1278/85305
        # 密钥可前往官网控制台 https://console.cloud.tencent.com/cam/capi 进行获取
        cred = credential.Credential(secretId, secretKey)
        # 实例化一个http选项，可选的，没有特殊需求可以跳过
        httpProfile = HttpProfile()
        httpProfile.endpoint = "sms.tencentcloudapi.com"

        # 实例化一个client选项，可选的，没有特殊需求可以跳过
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        # 实例化要请求产品的client对象,clientProfile是可选的
        client = sms_client.SmsClient(cred, "ap-nanjing", clientProfile)

        # 实例化一个请求对象,每个接口都会对应一个request对象
        req = models.SendSmsRequest()
        params = {
            "SmsSdkAppId": SmsSdkAppId,
            "SignName": SignName,
            "TemplateId": TemplateId,
            "TemplateParamSet": TemplateParamSet,
            "PhoneNumberSet": PhoneNumberSet
        }
        req.from_json_string(json.dumps(params))

        # 返回的resp是一个SendSmsResponse的实例，与请求对象对应
        resp = client.SendSms(req)
        print("resp:", resp.SendStatusSet[0].Code)
        # 输出json格式的字符串回包
        print("发送短信：", datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "result:", resp.to_json_string(), flush=True)

    except TencentCloudSDKException as err:
        print("短信出错：", err, flush=True)