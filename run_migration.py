from app.migrations.migrate_neo4j import run_migration
from app.database import close_neo4j_driver

if __name__ == "__main__":
    run_migration()
    close_neo4j_driver()