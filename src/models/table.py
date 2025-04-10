from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from src.database import Base


class TablesORM(Base):
    __tablename__ = "tables"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    seats: Mapped[int]
    location: Mapped[str] = mapped_column(String(100))