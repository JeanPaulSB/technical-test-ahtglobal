from sqlalchemy import Column, Integer, String, Text
from .database import Base


class Product(Base):
    __tablename__ = "inventory"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    mac_address = Column(String(100), unique=True)
    serial_number = Column(String(100), unique=True)
    manufacturer = Column(String(100))
    description = Column(Text)

    def __init__(
        self,
        name=None,
        mac_address=None,
        serial_number=None,
        manufacturer=None,
        description=None,
    ):
        self.name = name
        self.mac_address = mac_address
        self.serial_number = serial_number
        self.manufacturer = manufacturer
        self.description = description

    def __repr__(self):
        return f"<Product {self.serial_number}>"
