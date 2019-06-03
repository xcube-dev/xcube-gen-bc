import unittest

from xcube_gen_bc import init_plugin


class SnapPluginTest(unittest.TestCase):

    # noinspection PyMethodMayBeStatic
    def test_init_plugin(self):
        # Smoke test
        init_plugin()
