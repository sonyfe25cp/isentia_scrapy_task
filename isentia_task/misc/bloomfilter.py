# -*- coding: utf-8 -*-

from pybloom import BloomFilter
from scrapy.utils.job import job_dir
from scrapy.dupefilters import BaseDupeFilter
import logging

logger = logging.getLogger(__name__)

class BLOOMDupeFilter(BaseDupeFilter):
    """Request Fingerprint duplicates filter"""

    def __init__(self, path=None):
        self.file = None
        self.fingerprints = BloomFilter(2000000, 0.00001)

    @classmethod
    def from_settings(cls, settings):
        return cls(job_dir(settings))

    def request_seen(self, request):
        fp = request.url
        if fp in self.fingerprints:
            logger.debug('%s is seen', request.url)
            return True
        self.fingerprints.add(fp)
        

    def close(self, reason):
        self.fingerprints = None