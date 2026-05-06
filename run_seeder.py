from app.seeders.seed_dummy_data import run_seeder
from app.database import close_neo4j_driver

if __name__ == "__main__":
    run_seeder(clear_existing=True)
    close_neo4j_driver()