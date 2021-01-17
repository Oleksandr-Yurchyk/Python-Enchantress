import unittest
from homework import test_simple_calc as calc


class SimpleCalcTestCase(unittest.TestCase):
    """Test case for main calculator functions"""

    def test_add_positive_numbers(self):
        self.assertEqual(calc.add(3, 8), 11)

    def test_add_negative_numbers(self):
        self.assertEqual(calc.add(-7, -6), -13)

    def test_subtract_positive_numbers(self):
        self.assertEqual(calc.subtract(12, 5), 7)

    def test_subtract_negative_numbers(self):
        self.assertEqual(calc.subtract(-3, -10), 7)

    def test_multiply_positive_numbers(self):
        self.assertEqual(calc.multiply(7, 8), 56)

    def test_multiply_negative_numbers(self):
        self.assertEqual(calc.multiply(-7, -8), 56)

    def test_multiply_by_zero(self):
        self.assertEqual(calc.multiply(4, 0), 0)

    def test_divide_positive_numbers(self):
        self.assertEqual(calc.divide(10, 5), 2)

    def test_divide_negative_numbers(self):
        self.assertEqual(calc.divide(-10, -5), 2)

    def test_divide_failed(self):
        self.assertRaises(ValueError, lambda: calc.divide(3, 0))


if __name__ == '__main__':
    unittest.main()
