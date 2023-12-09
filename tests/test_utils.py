from unittest import TestCase

from source.utils import camel_case_possibilities


class Test(TestCase):
    def test_camel_case_possibilities(self):
        self.assertEqual(camel_case_possibilities("test"), ["test"])
        self.assertEqual(camel_case_possibilities("another_one"), ["anotherOne"])
        self.assertEqual(camel_case_possibilities("one_more_uuid"), ["oneMoreUuid", "oneMoreUUID"])

    def test_require(self):
        pass
