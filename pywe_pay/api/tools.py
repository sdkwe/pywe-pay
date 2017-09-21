# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from pywe_pay.base import BaseWeChatPayAPI


class WeChatTools(BaseWeChatPayAPI):

    def short_url(self, long_url):
        """
        长链接转短链接

        :param long_url: 长链接
        :return: 返回的结果数据
        """
        data = {
            'appid': self.appid,
            'long_url': long_url,
        }
        return self._post('/tools/shorturl', data=data)

    def auto_code_to_openid(self, auth_code):
        """
        授权码查询 openid 接口

        :param auth_code: 扫码支付授权码，设备读取用户微信中的条码或者二维码信息
        :return: 返回的结果数据
        """
        data = {
            'appid': self.appid,
            'auth_code': auth_code,
        }
        return self._post('/tools/authcodetoopenid', data=data)
