from db.db_client import init_db
from db.seed_data import seed
from agents.main_agent import run_agent

if __name__ == "__main__":
    init_db()
    seed()
    run_agent()