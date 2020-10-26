from django.test import TestCase

class TransactionListViewTest(TestCase):
    def setUp(self):
        import myapp.views
        myapp.views._transaction_list = {}
        return super().setUp()

    def test_get_empty_list(self):
        response = self.client.get('/api/transactions/')
        self.assertEqual(200, response.status_code)
        self.assertEqual([], response.json())

    def test_post_new(self):
        response = self.client.post('/api/transactions/', {'type': 'credit','amount': 10.5})
        self.assertEqual(201, response.status_code)
        response_data = response.json()
        self.assertEqual('credit', response_data['type'])
        self.assertEqual('10.50', response_data['amount'])
        self.assertIsNotNone(response_data['id'])
        self.assertIsNotNone(response_data['effective_date'])
    
    def test_negative_post(self):
        response = self.client.post('/api/transactions/', {'type': 'credit','amount': -10.5})
        self.assertEqual(422, response.status_code)

    def test_do_not_allow_negative_balance(self):
        response = self.client.post('/api/transactions/', {'type': 'credit','amount': 10.5})
        self.assertEqual(201, response.status_code)
        response = self.client.post('/api/transactions/', {'type': 'debit','amount': 10.5})
        self.assertEqual(201, response.status_code)

        response = self.client.post('/api/transactions/', {'type': 'debit','amount': 10.5})
        self.assertEqual(422, response.status_code)
    
    def test_get_list(self):
        self.client.post('/api/transactions/', {'type': 'credit','amount': 10.5})
        self.client.post('/api/transactions/', {'type': 'debit','amount': 9.25})
        response = self.client.get('/api/transactions/')
        self.assertEqual(200, response.status_code)

        response_data = response.json()
        self.assertEqual(2, len(response_data))


class TransactionDetailViewTest(TestCase):
    def setUp(self):
        import myapp.views
        myapp.views._transaction_list = {}
        return super().setUp()

    def test_get_by_id(self):
        response = self.client.post('/api/transactions/', {'type': 'credit','amount': 10.5})
        response = self.client.get('/api/transactions/{0}/'.format(response.json()['id']))
        self.assertEqual(200, response.status_code)


class AccountBalanceViewTest(TestCase):
    def setUp(self):
        import myapp.views
        myapp.views._transaction_list = {}
        return super().setUp()

    def test_get_account_balance(self):
        self.client.post('/api/transactions/', {'type': 'credit','amount': 10.5})
        self.client.post('/api/transactions/', {'type': 'debit','amount': 9.25})
        response = self.client.get('/api/default/')
        self.assertEqual(200, response.status_code)
        self.assertEquals(1.25, response.json()['balance'])