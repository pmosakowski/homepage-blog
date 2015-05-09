from django.test import TestCase

import django.utils.timezone as tz
import .templatetags.mytags as mt

class MyTagTest(TestCase):
    def setUp(self):
        self.now = tz.now();

    def test_humandate_filter(self):
        self.assertEqual(mt.humandate(self.now), "Today")
