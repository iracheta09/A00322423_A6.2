from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional

from src.customer import CustomerRepository
from src.hotel import HotelRepository
from src.storage import load_json, save_json


DATA_PATH = Path("data/reservations.json")


@dataclass
class Reservation:
    reservation_id: str
    customer_id: str
    hotel_id: str
    active: bool = True


class ReservationRepository:
    def __init__(
        self,
        path: Path = DATA_PATH,
        customer_repo: Optional[CustomerRepository] = None,
        hotel_repo: Optional[HotelRepository] = None,
    ) -> None:
        self.path = path
        self.customer_repo = customer_repo or CustomerRepository()
        self.hotel_repo = hotel_repo or HotelRepository()

    def _load(self) -> Dict[str, Reservation]:
        raw = load_json(self.path, default=[])
        reservations: Dict[str, Reservation] = {}

        if not isinstance(raw, list):
            print(f"[reservation] Invalid data format in '{self.path}'")
            return reservations

        for item in raw:
            if not isinstance(item, dict):
                continue

            rid = item.get("reservation_id")
            cid = item.get("customer_id")
            hid = item.get("hotel_id")
            active = item.get("active", True)

            if (
                isinstance(rid, str)
                and isinstance(cid, str)
                and isinstance(hid, str)
                and isinstance(active, bool)
            ):
                reservations[rid] = Reservation(
                    reservation_id=rid,
                    customer_id=cid,
                    hotel_id=hid,
                    active=active,
                )

        return reservations

    def _save(self, reservations: Dict[str, Reservation]) -> None:
        payload = [asdict(r) for r in reservations.values()]
        save_json(self.path, payload)

    def create_reservation(
        self, reservation_id: str, customer_id: str, hotel_id: str
    ) -> Reservation:
        reservation_id = (reservation_id or "").strip()
        customer_id = (customer_id or "").strip()
        hotel_id = (hotel_id or "").strip()

        if not reservation_id:
            raise ValueError("reservation_id must not be empty")
        if not customer_id:
            raise ValueError("customer_id must not be empty")
        if not hotel_id:
            raise ValueError("hotel_id must not be empty")

        reservations = self._load()
        if reservation_id in reservations:
            raise ValueError("reservation_id already exists")

        if self.customer_repo.get_customer(customer_id) is None:
            raise KeyError("customer_id not found")

        if self.hotel_repo.get_hotel(hotel_id) is None:
            raise KeyError("hotel_id not found")

        # Will raise if no rooms available
        self.hotel_repo.reserve_room(hotel_id)

        reservation = Reservation(
            reservation_id=reservation_id,
            customer_id=customer_id,
            hotel_id=hotel_id,
            active=True,
        )
        reservations[reservation_id] = reservation
        self._save(reservations)
        return reservation

    def get_reservation(self, reservation_id: str) -> Optional[Reservation]:
        reservations = self._load()
        return reservations.get(reservation_id)

    def cancel_reservation(self, reservation_id: str) -> None:
        reservations = self._load()

        if reservation_id not in reservations:
            raise KeyError("reservation_id not found")

        reservation = reservations[reservation_id]

        if not reservation.active:
            raise ValueError("reservation already canceled")

        reservation.active = False
        reservations[reservation_id] = reservation
        self._save(reservations)

        # Release room back
        self.hotel_repo.release_room(reservation.hotel_id)

    def list_reservations(self) -> List[Reservation]:
        reservations = self._load()
        return list(reservations.values())