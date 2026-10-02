import os
from neo4j import GraphDatabase

NEO4J_URI=os.getenv("NEO4J_URI","bolt://neo4j:7687")
NEO4J_USER=os.getenv("NEO4J_USER","node4j")
NEO4J_PASSWORD=os.getenv("NEO4J_PASSWORD","password")


driver=GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USER,NEO4J_PASSWORD)
)

def verify_connection():
    with driver.session() as session:
        result=session.run("RETURN 1 as result")
        return result.single()["result"]