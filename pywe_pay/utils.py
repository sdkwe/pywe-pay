# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import socket

import six
from pywe_utils import to_text


def dict_to_xml(d, sign):
    xml = ['<xml>\n']
    for k in sorted(d):
        # use sorted to avoid test error on Py3k
        v = d[k]
        if isinstance(v, six.integer_types) or v.isdigit():
            xml.append('<{0}>{1}</{0}>\n'.format(to_text(k), to_text(v)))
        else:
            xml.append(
                '<{0}><![CDATA[{1}]]></{0}>\n'.format(to_text(k), to_text(v))
            )
    xml.append('<sign><![CDATA[{0}]]></sign>\n</xml>'.format(to_text(sign)))
    return ''.join(xml)


def get_external_ip():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        wechat_ip = socket.gethostbyname('api.mch.weixin.qq.com')
        sock.connect((wechat_ip, 80))
        addr, port = sock.getsockname()
        sock.close()
        return addr
    except socket.error:
        return '127.0.0.1'


def timezone(zone):
    """Try to get timezone using pytz or python-dateutil

    :param zone: timezone str
    :return: timezone tzinfo or None
    """
    try:
        import pytz
        return pytz.timezone(zone)
    except ImportError:
        pass
    try:
        from dateutil.tz import gettz
        return gettz(zone)
    except ImportError:
        return None
