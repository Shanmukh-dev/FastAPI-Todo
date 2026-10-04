from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base # sessionmaker allows to talk to the datsbase, declarative_base is used to declare data models
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False)
Base = declarative_base()