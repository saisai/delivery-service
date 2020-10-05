from datetime import datetime

from django.test import TestCase
import requests
from models import CashierShift


class CashierTestCase(TestCase):

    def authorization(self):
        response = requests.post(
            'http://localhost:8000/api/token-auth/',
            headers={"Content-Type": "application/json"},
            data={
                "username": "courier_1",
                "password": "asdasd"
            },
        )
        self.token = response['token']

    def setUp(self) -> None:
        self.cashier = CashierShift.objects.create()
        self.token = None
        self.today = datetime.now().date()

    def test_cashier_start_shift(self):
        pass
