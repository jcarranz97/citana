"""Idempotent seed script — Phase 1 placeholder.

Currently only ensures the admin user exists by piggybacking on the same
bootstrap logic the app uses on startup. As more domains land
(customers, services, resources), extend this to load `seed_data.yaml`
sections similarly to colony's `scripts/seed_db.py`.
"""

import app.appointments.models
import app.auth.models  # noqa: F401
from app.database import Base, engine
from app.main import _bootstrap_admin


def seed() -> None:
    """Create tables and bootstrap the default admin user."""
    print("Creating tables (idempotent)...")
    Base.metadata.create_all(bind=engine)
    print("Bootstrapping default admin user (idempotent)...")
    _bootstrap_admin()
    print("Seed complete.")


if __name__ == "__main__":
    seed()
