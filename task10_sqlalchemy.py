from sqlalchemy import Float, String, create_engine, select
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
)


class Base(DeclarativeBase):
    pass


class Product(Base):
    """Модель товара."""

    __tablename__ = "products"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[float] = mapped_column(Float)

    def __repr__(self):
        return (
            f"Product(id={self.id}, "
            f"name='{self.name}', "
            f"price={self.price})"
        )


def main():
    engine = create_engine(
        "sqlite:///products.db",
        echo=False,
    )

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        products = [
            Product(name="Ноутбук", price=75000.0),
            Product(name="Мышь", price=2500.0),
            Product(name="Клавиатура", price=5000.0),
        ]

        session.add_all(products)
        session.commit()

    with Session(engine) as session:
        statement = select(Product)
        products = session.scalars(statement).all()

        print("Товары в базе данных:")

        for product in products:
            print(product)


if __name__ == "__main__":
    main()
