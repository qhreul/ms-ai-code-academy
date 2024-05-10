from pydantic import BaseModel, Field
from typing import Optional


class Person(BaseModel):
    ssn: str = Field(description='The social security number of the person')
    first_name: str = Field(description='The first name of the person')
    last_name: str = Field(description='The last name of the person')
    city: Optional[str] = Field(description='The city where the person lives')
    state: Optional[str] = Field(description='The state where the person lives')


class TaxForm(BaseModel):
    main_contributor: Person = Field(description='The main contributor of the tax form')
    spouse: Optional[Person] = Field(description='The spouse of the main contributor')
    taxable_amount: Optional[str] = Field(default='0', description='The amount of the tax form')
