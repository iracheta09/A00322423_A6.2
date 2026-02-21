"""Gestión de hoteles y disponibilidad de habitaciones en JSON."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional

from src.storage import load_json, save_json


DATA_PATH = Path("data/hotels.json")


@dataclass
class Hotel:
    """Entidad de hotel con capacidad total y habitaciones disponibles."""

    hotel_id: str
    name: str
    rooms_total: int
    rooms_available: int


class HotelRepository:
    """Repositorio para operaciones sobre hoteles y sus habitaciones."""

    def __init__(self, path: Path = DATA_PATH) -> None:
        """Inicializa el repositorio con la ruta de almacenamiento."""
        self.path = path

    def _load(self) -> Dict[str, Hotel]:
        """Carga hoteles desde JSON y devuelve un diccionario por ID."""
        raw = load_json(self.path, default=[])
        hotels: Dict[str, Hotel] = {}

        if not isinstance(raw, list):
            print(f"[hotel] Invalid data format in '{self.path}'")
            return hotels

        for item in raw:
            if not isinstance(item, dict):
                continue

            hid = item.get("hotel_id")
            name = item.get("name")
            total = item.get("rooms_total")
            available = item.get("rooms_available")

            if (
                isinstance(hid, str)
                and isinstance(name, str)
                and isinstance(total, int)
                and isinstance(available, int)
            ):
                hotels[hid] = Hotel(
                    hotel_id=hid,
                    name=name,
                    rooms_total=total,
                    rooms_available=available,
                )

        return hotels

    def _save(self, hotels: Dict[str, Hotel]) -> None:
        """Guarda el diccionario de hoteles en formato JSON."""
        payload = [asdict(h) for h in hotels.values()]
        save_json(self.path, payload)

    def create_hotel(self, hotel_id: str, name: str, rooms_total: int) -> Hotel:
        """Crea un hotel nuevo con todas sus habitaciones disponibles."""
        hotel_id = (hotel_id or "").strip()
        name = (name or "").strip()

        if not hotel_id:
            raise ValueError("hotel_id must not be empty")
        if not name:
            raise ValueError("name must not be empty")
        if rooms_total <= 0:
            raise ValueError("rooms_total must be greater than 0")

        hotels = self._load()

        if hotel_id in hotels:
            raise ValueError("hotel_id already exists")

        hotel = Hotel(
            hotel_id=hotel_id,
            name=name,
            rooms_total=rooms_total,
            rooms_available=rooms_total,
        )

        hotels[hotel_id] = hotel
        self._save(hotels)
        return hotel

    def get_hotel(self, hotel_id: str) -> Optional[Hotel]:
        """Obtiene un hotel por su ID o `None` si no existe."""
        hotels = self._load()
        return hotels.get(hotel_id)

    def reserve_room(self, hotel_id: str) -> None:
        """Reserva una habitación en el hotel indicado si hay disponibilidad."""
        hotels = self._load()

        if hotel_id not in hotels:
            raise KeyError("hotel_id not found")

        hotel = hotels[hotel_id]

        if hotel.rooms_available <= 0:
            raise ValueError("no rooms available")

        hotel.rooms_available -= 1
        self._save(hotels)

    def release_room(self, hotel_id: str) -> None:
        """Libera una habitación previamente reservada en el hotel indicado."""
        hotels = self._load()

        if hotel_id not in hotels:
            raise KeyError("hotel_id not found")

        hotel = hotels[hotel_id]

        if hotel.rooms_available >= hotel.rooms_total:
            raise ValueError("all rooms already available")

        hotel.rooms_available += 1
        self._save(hotels)

    def list_hotels(self) -> List[Hotel]:
        """Lista todos los hoteles almacenados."""
        hotels = self._load()
        return list(hotels.values())
