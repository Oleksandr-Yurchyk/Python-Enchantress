import unittest
from unittest import mock
from homework.tests_complex import func, Test, new_test


class ComplexTestCase(unittest.TestCase):

    def setUp(self):
        self.test = Test()
        print('Enter to test func')

    def tearDown(self):
        print("Exit from test func")
        pass

    def test_enter(self):
        self.assertEqual(self.test.__enter__(), self.test)

    @mock.patch('homework.tests_complex.Test.__exit__', return_value=True)
    def test_exit(self, test):
        self.assertEqual(self.test.__exit__(1, 1, 1), True)

    def test_hello(self):
        self.assertEqual(func(), 1)

    @mock.patch('homework.tests_complex.Test.hello', return_value='Changed value')
    def test_hello_with_mock(self, request):
        self.assertEqual(self.test.hello(), 'Changed value')

    def test_new_test(self):
        self.assertIsInstance(new_test(), Test)


if __name__ == '__main__':
    unittest.main()
