import unittest
from pathlib import Path
import tempfile

from src.customer import CustomerRepository
from src.hotel import HotelRepository
from src.reservation import ReservationRepository


class TestReservationRepository(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)

        self.customers_path = base / "customers.json"
        self.hotels_path = base / "hotels.json"
        self.reservations_path = base / "reservations.json"

        self.customer_repo = CustomerRepository(path=self.customers_path)
        self.hotel_repo = HotelRepository(path=self.hotels_path)
        self.repo = ReservationRepository(
            path=self.reservations_path,
            customer_repo=self.customer_repo,
            hotel_repo=self.hotel_repo,
        )

        self.customer_repo.create_customer("C1", "Cesar")
        self.hotel_repo.create_hotel("H1", "Hotel WYNY", 1)

    def tearDown(self):
        self.tmp.cleanup()

    def test_create_reservation_success(self):
        r = self.repo.create_reservation("R1", "C1", "H1")
        self.assertTrue(r.active)

        hotel = self.hotel_repo.get_hotel("H1")
        self.assertEqual(hotel.rooms_available, 0)

    def test_create_reservation_customer_not_found(self):
        with self.assertRaises(KeyError):
            self.repo.create_reservation("R1", "X", "H1")

    def test_create_reservation_hotel_not_found(self):
        with self.assertRaises(KeyError):
            self.repo.create_reservation("R1", "C1", "X")

    def test_create_reservation_no_rooms_available(self):
        self.repo.create_reservation("R1", "C1", "H1")
        with self.assertRaises(ValueError):
            self.repo.create_reservation("R2", "C1", "H1")

    def test_cancel_reservation_releases_room(self):
        self.repo.create_reservation("R1", "C1", "H1")
        self.repo.cancel_reservation("R1")

        r = self.repo.get_reservation("R1")
        self.assertFalse(r.active)

        hotel = self.hotel_repo.get_hotel("H1")
        self.assertEqual(hotel.rooms_available, 1)

    def test_cancel_nonexistent_raises(self):
        with self.assertRaises(KeyError):
            self.repo.cancel_reservation("X")

    def test_cancel_twice_raises(self):
        self.repo.create_reservation("R1", "C1", "H1")
        self.repo.cancel_reservation("R1")
        with self.assertRaises(ValueError):
            self.repo.cancel_reservation("R1")


if __name__ == "__main__":
    unittest.main()