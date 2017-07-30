# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import random
from datetime import datetime


class BaseWeChatPayAPI(object):
    """ WeChat Pay API base class """
    def __init__(self, client=None):
        self._client = client

    def _get(self, url, **kwargs):
        if getattr(self, 'API_BASE_URL', None):
            kwargs['api_base_url'] = self.API_BASE_URL
        return self._client.get(url, **kwargs)

    def _post(self, url, **kwargs):
        if getattr(self, 'API_BASE_URL', None):
            kwargs['api_base_url'] = self.API_BASE_URL
        return self._client.post(url, **kwargs)

    @property
    def appid(self):
        return self._client.appid

    @property
    def mch_id(self):
        return self._client.mch_id

    @property
    def sub_mch_id(self):
        return self._client.sub_mch_id

    @property
    def out_trade_no(self):
        return '{0}{1}{2}'.format(
            self.mch_id,
            datetime.now().strftime('%Y%m%d%H%M%S'),
            random.randint(1000, 10000)
        )
