from fastapi import FastAPI
from pydantic import BaseModel
from .database import driver, verify_connection
from .models import Timesheet,Employee
from .extraction import extract_entities
app = FastAPI(title="WorkGraph AI")


class Employee(BaseModel):
    id: str
    name: str


@app.get("/")
def root():
    return {
        "message": "WorkGraph AI backend is running"
    }


@app.get("/health")
def health():
    try:
        result = verify_connection()

        return {
            "status": "healthy",
            "neo4j": result == 1
        }

    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }


@app.post("/employees")
def create_employee(employee: Employee):

    query = """
    MERGE (e:Employee {id: $id})
    SET e.name = $name
    RETURN e.id AS id, e.name AS name
    """

    with driver.session() as session:
        result = session.run(
            query,
            id=employee.id,
            name=employee.name
        )

        record = result.single()

        return {
            "id": record["id"],
            "name": record["name"]
        }

@app.post("/Timesheet")
def create_timesheet(timesheet:Timesheet):
    extract=extract_entities(timesheet.description)
    query = """
    MATCH (e:Employee {id: $employee_id})

    CREATE (e)-[:SUBMITTED]->(t:Timesheet {
        employee_id: $employee_id,
        date: $date,
        hours: $hours,
        description: $description
    })

    WITH e, t

    FOREACH (skill IN $skills |
        MERGE (s:Skill {name: skill})
        MERGE (e)-[:HAS_SKILL]->(s)
        MERGE (t)-[:INVOLVES]->(s)
    )

    FOREACH (tool IN $tools |
        MERGE (tl:Tool {name: tool})
        MERGE (e)-[:KNOWS_TOOL]->(tl)
        MERGE (t)-[:USES]->(tl)
    )

    RETURN e.id AS employee_id
    """

    with driver.session() as session:
        result=session.run(
            query,
            employee_id=timesheet.employee_id,
            date=timesheet.date,
            hours=timesheet.hours,
            description=timesheet.description,
            skills=extract["skills"],
            tools=extract["tools"]
        )
        record=result.single()

        return {
            "message":"Timesheet created successfully",
            "employee_id":record["employee_id"],
            "extract":extract
        }