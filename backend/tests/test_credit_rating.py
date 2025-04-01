import unittest
from unittest.mock import patch
from credit_rating import CreditRating


class TestCreditRating(unittest.TestCase):
    @patch('credit_rating.db.session.query')
    def test_calculate_credit_rating_AAA(self, mock_query):
        mock_query.return_value.scalar.return_value = 0
        c = CreditRating()

        result = c.calculate_credit_rating(
            750, 100000, 120000, 50000, 20000, 'fixed', 'single_family'
        )
        self.assertEqual(result, "AAA")

    @patch('credit_rating.db.session.query')
    def test_calculate_credit_rating_BBB(self, mock_query):
        mock_query.return_value.scalar.return_value = 700
        c = CreditRating()

        result = c.calculate_credit_rating(
            400, 234234, 32424, 234234, 234234, 'fixed', 'single_family'
        )
        self.assertEqual(result, 'BBB')

    @patch('credit_rating.db.session.query')
    def test_calculate_credit_rating_C(self, mock_query):
        mock_query.return_value.scalar.return_value = 720
        c = CreditRating()

        result = c.calculate_credit_rating(
            620, 120000, 100000, 40000, 25000, 'Adjustable', 'Condo'
        )
        self.assertEqual(result, "C")
