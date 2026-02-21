"""Gestión de clientes y persistencia en almacenamiento JSON."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional

from src.storage import load_json, save_json


DATA_PATH = Path("data/customers.json")


@dataclass
class Customer:
    """Entidad de cliente identificada por ID y nombre."""

    customer_id: str
    name: str


class CustomerRepository:
    """Repositorio para operaciones CRUD de clientes."""

    def __init__(self, path: Path = DATA_PATH) -> None:
        """Inicializa el repositorio con la ruta de almacenamiento."""
        self.path = path

    def _load(self) -> Dict[str, Customer]:
        """Carga clientes desde JSON y devuelve un diccionario por ID."""
        raw = load_json(self.path, default=[])
        customers: Dict[str, Customer] = {}

        if not isinstance(raw, list):
            print(f"[customer] Invalid data format in '{self.path}'")
            return customers

        for item in raw:
            if not isinstance(item, dict):
                continue

            cid = item.get("customer_id")
            name = item.get("name")

            if isinstance(cid, str) and isinstance(name, str):
                customers[cid] = Customer(customer_id=cid, name=name)

        return customers

    def _save(self, customers: Dict[str, Customer]) -> None:
        """Guarda el diccionario de clientes en formato JSON."""
        payload = [asdict(c) for c in customers.values()]
        save_json(self.path, payload)

    def create_customer(self, customer_id: str, name: str) -> Customer:
        """Crea un cliente nuevo validando campos obligatorios y unicidad."""
        customer_id = (customer_id or "").strip()
        name = (name or "").strip()

        if not customer_id:
            raise ValueError("customer_id must not be empty")
        if not name:
            raise ValueError("name must not be empty")

        customers = self._load()

        if customer_id in customers:
            raise ValueError("customer_id already exists")

        customer = Customer(customer_id=customer_id, name=name)
        customers[customer_id] = customer
        self._save(customers)
        return customer

    def get_customer(self, customer_id: str) -> Optional[Customer]:
        """Obtiene un cliente por su ID o `None` si no existe."""
        customers = self._load()
        return customers.get(customer_id)

    def update_customer(self, customer_id: str, name: str) -> Customer:
        """Actualiza el nombre de un cliente existente."""
        name = (name or "").strip()

        if not name:
            raise ValueError("name must not be empty")

        customers = self._load()

        if customer_id not in customers:
            raise KeyError("customer_id not found")

        customers[customer_id].name = name
        self._save(customers)
        return customers[customer_id]

    def delete_customer(self, customer_id: str) -> None:
        """Elimina un cliente existente por su ID."""
        customers = self._load()

        if customer_id not in customers:
            raise KeyError("customer_id not found")

        del customers[customer_id]
        self._save(customers)

    def list_customers(self) -> List[Customer]:
        """Lista todos los clientes almacenados."""
        customers = self._load()
        return list(customers.values())
