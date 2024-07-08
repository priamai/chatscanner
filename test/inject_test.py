import unittest
from .victimapp_simple import demo

class InjectCase(unittest.TestCase):
    def test_app(self):
        demo.launch(share=False,debug=True)


if __name__ == '__main__':
    unittest.main()
