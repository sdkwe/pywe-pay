# -*- coding: utf-8 -*-

import inspect
import sys

import requests
from pywe_base import BaseWechat
from pywe_exception import WeChatPayException
from pywe_pay.api.bill import WeChatBill
from pywe_pay.api.coupon import WeChatCoupon
from pywe_pay.api.jsapi import WeChatJSAPI
from pywe_pay.api.micropay import WeChatMicroPay
from pywe_pay.api.order import WeChatOrder
from pywe_pay.api.redpack import WeChatRedpack
from pywe_pay.api.refund import WeChatRefund
from pywe_pay.api.tools import WeChatTools
from pywe_pay.api.transfer import WeChatTransfer
from pywe_pay.base import BaseWeChatPayAPI
from pywe_sign import calculate_signature
from pywe_utils import random_string
from pywe_xml import dict_to_xml, xml_to_dict


def _is_api_endpoint(obj):
    return isinstance(obj, BaseWeChatPayAPI)


class WeChatPay(BaseWechat):
    billl = WeChatBill()
    coupon = WeChatCoupon()
    jsapi = WeChatJSAPI()
    micropay = WeChatMicroPay()
    order = WeChatOrder()
    redpack = WeChatRedpack()
    refund = WeChatRefund()
    tools = WeChatTools()
    transfer = WeChatTransfer()

    def __new__(cls, *args, **kwargs):
        self = super(WeChatPay, cls).__new__(cls)
        if sys.version_info[:2] == (2, 6):
            import copy
            # Python 2.6 inspect.gemembers bug workaround
            # http://bugs.python.org/issue1785
            for name, _api in self.__class__.__dict__.items():
                if isinstance(_api, BaseWeChatPayAPI):
                    _api = copy.deepcopy(_api)
                    _api._client = self
                    setattr(self, name, _api)
        else:
            api_endpoints = inspect.getmembers(self, _is_api_endpoint)
            for name, _api in api_endpoints:
                api_cls = type(_api)
                _api = api_cls(self)
                setattr(self, name, _api)
        return self

    def __init__(self, appid, api_key, mch_id, sub_mch_id=None, mch_cert=None, mch_key=None):
        # 微信支付开发文档, Refer: https://pay.weixin.qq.com/wiki/doc/api/index.html
        # 扫码支付： 用户打开"微信扫一扫“，扫描商户的二维码后完成支付
        # 公众号支付： 用户在微信内进入商家H5页面，页面内调用JSSDK完成支付
        # APP 支付： 商户APP中集成微信SDK，用户点击后跳转到微信内完成支付
        """
        :param appid: 微信公众号 appid
        :param api_key: 商户 key
        :param mch_id: 商户号
        :param sub_mch_id: 可选，子商户号，受理模式下必填
        :param mch_cert: 可选，商户证书路径
        :param mch_key: 可选，商户证书私钥路径
        """
        super(WeChatPay, self).__init__()
        self.appid = appid
        self.api_key = api_key
        self.mch_id = mch_id
        self.sub_mch_id = sub_mch_id
        self.mch_cert = mch_cert
        self.mch_key = mch_key

    def __request(self, method, endpoint, **kwargs):
        if isinstance(kwargs.get('data', ''), dict):
            data = kwargs['data']
            if 'mchid' not in data:
                data.setdefault('mch_id', self.mch_id)
            data.setdefault('sub_mch_id', self.sub_mch_id)
            data.setdefault('nonce_str', random_string(32))
            data['sign'] = calculate_signature(data, self.api_key)
            body = dict_to_xml(data)
            body = body.encode('utf-8')
            kwargs['data'] = body

        # 商户证书
        if self.mch_cert and self.mch_key:
            kwargs['cert'] = (self.mch_cert, self.mch_key)

        res = requests.request(
            method=method,
            url='{base}{endpoint}'.format(base=self.MCH_DOMAIN, endpoint=endpoint),
            verify=False,
            **kwargs
        )

        try:
            res.raise_for_status()
        except requests.RequestException as reqe:
            raise WeChatPayException(reqe)

        return self.__handle_result(res)

    def __handle_result(self, res):
        res.encoding = 'utf-8'
        xml = res.text

        data = xml_to_dict(xml)
        if isinstance(data, basestring):
            return xml

        if data['return_code'] != 'SUCCESS' or data.get('result_code') != 'SUCCESS':
            raise WeChatPayException(data)

        return data

    def get(self, url, **kwargs):
        return self.__request(method='get', endpoint=url, **kwargs)

    def post(self, url, **kwargs):
        return self.__request(method='post', endpoint=url, **kwargs)
