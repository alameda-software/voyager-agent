"""Load wedding vendors from JSON file into the database."""

import asyncio
import json
from pathlib import Path

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.models import Vendor


async def load_vendors():
    """Load vendors from JSON and insert into database."""

    # Load JSON file
    vendors_path = Path(__file__).parent.parent / "domains" / "wedding" / "data" / "vendors.json"
    with open(vendors_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    vendors_data = data.get("vendors", [])
    print(f"📚 Loaded {len(vendors_data)} vendors from {vendors_path}")

    # Create async engine and session
    engine = create_async_engine(settings.database_url, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        # Clear existing vendors
        await session.execute(text("DELETE FROM wedding_vendors"))
        print("🗑️  Cleared existing vendors")

        valid_cols = {c.key for c in Vendor.__table__.columns}
        vendors = []
        for vendor_data in vendors_data:
            filtered = {k: v for k, v in vendor_data.items() if k in valid_cols}
            vendor = Vendor(**filtered)
            vendors.append(vendor)

        session.add_all(vendors)
        await session.commit()
        print(f"✅ Inserted {len(vendors)} vendors into database")

        # Verify count
        result = await session.execute(text("SELECT COUNT(*) FROM wedding_vendors"))
        count = result.scalar()
        print(f"📊 Database now contains {count} vendors")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(load_vendors())
