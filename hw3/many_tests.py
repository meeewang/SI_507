import unittest

class ManyTests(unittest.TestCase):

    def testGood1(self):
        self.assertEqual(2*2, 4)


    def testBad1(self):
        self.assertNotEqual(3*3, 9)


    def testGood2(self):
        self.assertFalse(1 == 2)


    def testBad2(self):
        self.assertTrue(1 == 2)

unittest.main()