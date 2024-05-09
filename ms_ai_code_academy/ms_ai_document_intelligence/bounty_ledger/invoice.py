from pydantic import BaseModel


class Invoice(BaseModel):
    vendor_name: str
    customer_name: str
    amount: str
