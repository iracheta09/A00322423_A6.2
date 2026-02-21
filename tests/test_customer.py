import unittest
from pathlib import Path
import tempfile

from src.customer import CustomerRepository


class TestCustomerRepository(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / "customers.json"
        self.repo = CustomerRepository(path=self.path)

    def tearDown(self):
        self.tmp.cleanup()

    def test_create_and_get_customer(self):
        self.repo.create_customer("C1", "Cesar")
        customer = self.repo.get_customer("C1")
        self.assertIsNotNone(customer)
        self.assertEqual(customer.customer_id, "C1")
        self.assertEqual(customer.name, "Cesar")

    def test_duplicate_customer_id_raises(self):
        self.repo.create_customer("C1", "Cesar")
        with self.assertRaises(ValueError):
            self.repo.create_customer("C1", "Otro")

    def test_empty_name_raises(self):
        with self.assertRaises(ValueError):
            self.repo.create_customer("C1", "")

    def test_update_customer(self):
        self.repo.create_customer("C1", "Cesar")
        updated = self.repo.update_customer("C1", "Cesar Iracheta")
        self.assertEqual(updated.name, "Cesar Iracheta")

    def test_update_nonexistent_raises(self):
        with self.assertRaises(KeyError):
            self.repo.update_customer("X", "Name")

    def test_delete_customer(self):
        self.repo.create_customer("C1", "Cesar")
        self.repo.delete_customer("C1")
        self.assertIsNone(self.repo.get_customer("C1"))

    def test_delete_nonexistent_raises(self):
        with self.assertRaises(KeyError):
            self.repo.delete_customer("X")

    def test_list_customers(self):
        self.repo.create_customer("C1", "Cesar")
        self.repo.create_customer("C2", "Ana")
        customers = self.repo.list_customers()
        self.assertEqual(len(customers), 2)


if __name__ == "__main__":
    unittest.main()
