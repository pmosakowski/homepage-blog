from django.test import TestCase

import django.utils.timezone as tz
from .templatetags import mytags as mt

class MyTagTest(TestCase):
    def setUp(self):
        self.now = tz.now();

    def test_humandate_filter(self):
        self.assertEqual(mt.humandate(self.now), "Today")
