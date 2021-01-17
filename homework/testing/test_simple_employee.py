import unittest
from unittest.mock import patch
from homework.tests_simple_employee import Employee


class SimpleEmployeeTestCase(unittest.TestCase):
    """Test case for Employee class functions"""

    def setUp(self):
        self.employee = Employee('Dmytro', 'Gordon', 1000)

    def test_correctly_instance_created(self):
        self.assertEqual(self.employee.first, 'Dmytro')
        self.assertEqual(self.employee.last, 'Gordon')
        self.assertEqual(self.employee.pay, 1000)

    def test_email(self):
        self.assertEqual(self.employee.email, 'Dmytro.Gordon@email.com')

    def test_fullname(self):
        self.assertEqual(self.employee.fullname, 'Dmytro Gordon')

    def test_apply_raise(self):
        self.employee.apply_raise()
        self.assertEqual(self.employee.pay, 1050)

    def test_monthly_schedule_bad_response(self):
        with patch('homework.tests_simple_employee.requests.get') as response:
            response.return_value.ok = False
            self.assertEqual(Employee.monthly_schedule(self.employee, 'June'), 'Bad Response!')

    def test_monthly_schedule_good_response(self):
        with patch('homework.tests_simple_employee.requests.get') as response:
            response.return_value.ok = True
            response.return_value.text = 'HTML Text'
            self.assertEqual(Employee.monthly_schedule(self.employee, 'June'), 'HTML Text')


if __name__ == '__main__':
    unittest.main()
