"""Seed data loader — inserts default playbook and admin user."""

import asyncio
import json
import uuid
from pathlib import Path

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

# Adjust sys.path so we can import app modules
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from app.config import settings  # noqa: E402
from app.core.security import hash_password  # noqa: E402
from app.models.user import User  # noqa: E402
from app.models.playbook import Playbook, PlaybookRule  # noqa: E402
from app.core.database import Base  # noqa: E402

SEED_DIR = Path(__file__).resolve().parent.parent / "data" / "seed"


async def seed():
    engine = create_async_engine(settings.database_url, echo=True)
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    async with session_factory() as session:
        # ── Admin User ───────────────────────────────────
        admin = User(
            id=uuid.uuid4(),
            email="admin@lagent.dev",
            password_hash=hash_password("AdminPass123!@#"),
            full_name="Lagent Admin",
            role="admin",
        )
        session.add(admin)
        await session.flush()

        # ── Default Playbook ─────────────────────────────
        playbook_data = json.loads((SEED_DIR / "default_playbook.json").read_text("utf-8"))
        playbook = Playbook(
            id=uuid.uuid4(),
            user_id=admin.id,
            name=playbook_data["name"],
            description=playbook_data["description"],
            is_default=playbook_data["is_default"],
        )
        session.add(playbook)
        await session.flush()

        for rule in playbook_data["rules"]:
            session.add(
                PlaybookRule(
                    id=uuid.uuid4(),
                    playbook_id=playbook.id,
                    rule_type=rule["rule_type"],
                    content=rule["content"],
                    threshold_value=rule.get("threshold_value"),
                )
            )

        await session.commit()
        print(f"✅  Admin user created: {admin.email}")
        print(f"✅  Default playbook created: {playbook.name} ({len(playbook_data['rules'])} rules)")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(seed())
