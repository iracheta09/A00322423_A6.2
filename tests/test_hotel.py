import unittest
from pathlib import Path
import tempfile

from src.hotel import HotelRepository


class TestHotelRepository(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / "hotels.json"
        self.repo = HotelRepository(path=self.path)

    def tearDown(self):
        self.tmp.cleanup()

    def test_create_hotel(self):
        hotel = self.repo.create_hotel("H1", "Hotel WYNY", 10)
        self.assertEqual(hotel.rooms_available, 10)

    def test_duplicate_hotel_raises(self):
        self.repo.create_hotel("H1", "Hotel WYNY", 10)
        with self.assertRaises(ValueError):
            self.repo.create_hotel("H1", "Otro", 5)

    def test_reserve_room(self):
        self.repo.create_hotel("H1", "Hotel WYNY", 2)
        self.repo.reserve_room("H1")
        hotel = self.repo.get_hotel("H1")
        self.assertEqual(hotel.rooms_available, 1)

    def test_reserve_no_rooms_raises(self):
        self.repo.create_hotel("H1", "Hotel WYNY", 1)
        self.repo.reserve_room("H1")
        with self.assertRaises(ValueError):
            self.repo.reserve_room("H1")

    def test_release_room(self):
        self.repo.create_hotel("H1", "Hotel WYNY", 2)
        self.repo.reserve_room("H1")
        self.repo.release_room("H1")
        hotel = self.repo.get_hotel("H1")
        self.assertEqual(hotel.rooms_available, 2)


if __name__ == "__main__":
    unittest.main()
