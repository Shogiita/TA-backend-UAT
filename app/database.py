from neo4j import GraphDatabase
from app import config

neo4j_driver = GraphDatabase.driver(
    config.NEO4J_URI,
    auth=(config.NEO4J_USER, config.NEO4J_PASSWORD)
)


def get_neo4j_session():
    return neo4j_driver.session(database=config.NEO4J_DATABASE)


def test_neo4j_connection():
    try:
        with get_neo4j_session() as session:
            result = session.run("RETURN 'Neo4j Aura connected' AS message")
            record = result.single()
            return record["message"] if record else "Neo4j connected"
    except Exception as e:
        return f"Neo4j connection failed: {str(e)}"


def close_neo4j_driver():
    neo4j_driver.close()