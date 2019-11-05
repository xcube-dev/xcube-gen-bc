import unittest

from xcube.util import extension
from xcube_gen_bc.plugin import init_plugin


class SnapPluginTest(unittest.TestCase):

    # noinspection PyMethodMayBeStatic
    def test_init_plugin(self):
        ext_reg = extension.ExtensionRegistry()
        init_plugin(ext_reg)
        self.assertTrue(ext_reg.has_extension('xcube.core.gen.iproc', 'snap-olci-highroc-l2'))
        self.assertTrue(ext_reg.has_extension('xcube.core.gen.iproc', 'snap-olci-cyanoalert-l2'))
