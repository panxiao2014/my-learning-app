from sqlalchemy import CheckConstraint, Identity, Integer, PrimaryKeyConstraint, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = 'users'
    __table_args__ = (
        CheckConstraint('age >= 0 AND age <= 100', name='users_age_check'),
        CheckConstraint("gender::text = ANY (ARRAY['Male'::character varying, 'Female'::character varying]::text[])", name='users_gender_check'),
        PrimaryKeyConstraint('id', name='users_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    name: Mapped[str] = mapped_column(String(40), nullable=False)
    gender: Mapped[str] = mapped_column(String(6), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
