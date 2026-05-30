import unittest

from slimepet_core import APP_NAME, APP_VERSION, clamp_position


class SlimePetCoreTest(unittest.TestCase):
    def test_app_metadata_is_current(self):
        self.assertEqual(APP_NAME, "SlimePet")
        self.assertEqual(APP_VERSION, "v0.0.4")

    def test_clamp_position_keeps_point_inside_bounds(self):
        self.assertEqual(clamp_position(-10, 120, 100, 80), (0, 80))
        self.assertEqual(clamp_position(40, 50, 100, 80), (40, 50))
        self.assertEqual(clamp_position(140, -20, 100, 80), (100, 0))


if __name__ == "__main__":
    unittest.main()
