# -*- coding: utf-8 -*-
from proxy import PROXIES
from agents import AGENTS

import random
import logging

logger = logging.getLogger(__name__)

"""
Custom http proxy middle ware, avoding banned
"""
class CustomHttpProxyMiddleware(object):

    def process_request(self, request, spider):
        if self.use_proxy(request, spider):
            p = random.choice(PROXIES)
            try:
                request.meta['proxy'] = "http://%s" % p['ip_port']
            except Exception, e:
                logger.error('error in Request is %s', e)

    def use_proxy(self, request, spider):
        """
        using direct download for depth <= 2
        using proxy with probability 0.3
        """
        if spider.settings.get('HTTP_PROXY_ENABLE'):
            if "depth" in request.meta and int(request.meta['depth']) <= 2:
                return False
            i = random.randint(1, 10)
            return i <= 2
        else:
            return False

"""
Custom user agent middleware, avoding banned
"""
class CustomUserAgentMiddleware(object):
    def process_request(self, request, spider):
        agent = random.choice(AGENTS)
        request.headers['User-Agent'] = agent
        logger.debug('%s is used for %s', agent, request.url)