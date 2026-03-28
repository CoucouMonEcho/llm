from typing import Annotated
from pydantic import BaseModel, Field, ValidationError

Age = Annotated[int, Field(ge=0, le=120, description="年龄0-120")]


class Person(BaseModel):
    name: str
    age: int
    age1: Age


try:
    p = Person(name="John", age="111", age1=200)
    print(p)
except ValidationError as e:
    print(e)

