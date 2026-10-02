from pydantic import BaseModel


class Employee(BaseModel):
    id: str
    name: str


class Timesheet(BaseModel):
    employee_id: str
    date: str
    hours: float
    description: str