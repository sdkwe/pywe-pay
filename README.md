# pywe-pay

Wechat Pay Module for Python.

# Installation

```shell
pip install pywe-pay
```

# Problems
* 201 商户订单号重复
  ```
  wxpay.order.create(body=u'测试', notify_url='https://a.com', out_trade_no=10, total_fee=100, trade_type='NATIVE')
  wxpay.order.create(body=u'测试', notify_url='https://a.com', out_trade_no=10, total_fee=1, trade_type='NATIVE')
  ```
