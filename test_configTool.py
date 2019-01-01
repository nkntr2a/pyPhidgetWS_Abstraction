from unittest import TestCase

from phidgetConfig import ConfigTool


class Test(TestCase):

    def setUp(self):
        try:
            self.cfg
        except AttributeError:
            self.cfg = ConfigTool("./phidgetConfig.json")

    def tearDown(self):
        self.assertTrue(True)

    def test_get_config_tool(self):
        val = self.cfg.get_config_tool()
        self.assertEqual(type(val), dict)

    def test_get_network_discovery(self):
        val = self.cfg.get_network_discovery()
        self.assertEqual(val, True)

    def test_get_is_sbc(self):
        val = self.cfg.get_is_sbc()
        self.assertEqual(val, True)

    def test_get_ip_address(self):
        val = self.cfg.get_ip_address()
        self.assertEqual(val, '192.168.1.211')

    def test_get_password(self):
        val = self.cfg.get_password()
        self.assertIsNone(val)

    def test_get_use_www_connect(self):
        val = self.cfg.get_use_www_connect()
        self.assertEqual(val, False)
