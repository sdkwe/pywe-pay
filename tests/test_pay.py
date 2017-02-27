# -*- coding: utf-8 -*-

import time

from local_config_example import WechatPayConfig
from pywe_pay import WeChatPay


class TestPayCommands(object):

    def test_native_unifiedorder(self):
        native = WechatPayConfig.get('JSAPI', {})
        wxpay = WeChatPay(native.get('appID'), native.get('apiKey'), native.get('mchID'))
        result = wxpay.order.create(body=u'支付测试', notify_url='https://a.com', out_trade_no=int(time.time() * 1000), total_fee=1, trade_type='NATIVE')
        assert isinstance(result, dict)
        assert result.get('return_code') == 'SUCCESS'
        assert result.get('result_code') == 'SUCCESS'
        assert result.get('code_url')
