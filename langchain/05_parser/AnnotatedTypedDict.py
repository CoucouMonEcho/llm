from typing import Annotated, TypedDict

Age = Annotated[int, "Age desc"]

class Person(TypedDict):
    name: str
    age: int
    age1: Age


p = Person(name="John", age="111", age1="222")
print(p)
