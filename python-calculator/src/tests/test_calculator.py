import unittest
from calculator import add, subtract, multiply, divide
from operations.basic import add, subtract, multiply, divide
from operations.advanced import power, square_root, logarithm

class TestCalculator(unittest.TestCase):

    def test_add(self):
        self.assertEqual(add(1, 2), 3)
        self.assertEqual(add(-1, 1), 0)
        self.assertEqual(add(-1, -1), -2)

    def test_subtract(self):
        self.assertEqual(subtract(2, 1), 1)
        self.assertEqual(subtract(1, 1), 0)
        self.assertEqual(subtract(-1, -1), 0)

    def test_multiply(self):
        self.assertEqual(multiply(2, 3), 6)
        self.assertEqual(multiply(-1, 1), -1)
        self.assertEqual(multiply(-1, -1), 1)

    def test_divide(self):
        self.assertEqual(divide(6, 3), 2)
        self.assertEqual(divide(1, 1), 1)
        with self.assertRaises(ZeroDivisionError):
            divide(1, 0)

    def test_power(self):
        self.assertEqual(power(2, 3), 8)
        self.assertEqual(power(5, 0), 1)

    def test_square_root(self):
        self.assertEqual(square_root(4), 2)
        with self.assertRaises(ValueError):
            square_root(-1)

    def test_logarithm(self):
        self.assertAlmostEqual(logarithm(100, 10), 2)
        with self.assertRaises(ValueError):
            logarithm(-1, 10)

if __name__ == '__main__':
    unittest.main()