# A00322423 - Actividad 6.2
## Ejercicio de programación 3 y pruebas de unidad

Repositorio con un sistema básico en Python para gestionar **clientes**, **hoteles** y **reservaciones**, incluyendo persistencia en archivos JSON, pruebas unitarias, cobertura y análisis estático.

## Estructura

- `src/`: implementación (customer, hotel, reservation, storage)
- `tests/`: pruebas unitarias con `unittest`
- `data/`: archivos JSON de persistencia
- `A00322423_A6_2.pdf`: reporte y evidencia (pruebas, coverage, flake8, pylint, commits)

## Requisitos

Instalar dependencias:

```bash
pip install -r requirements.txt

python -m unittest discover -s tests -p "test_*.py" -v

python -m coverage run -m unittest discover -s tests -p "test_*.py"
python -m coverage report -m

flake8 src tests
pylint src
