# db_conf.py

from sqlalchemy import create_engine, MetaData
from databases import Database  # ✅ ini dari library eksternal, bukan file lokal!

DATABASE_URL = "sqlite:///./siswa.db"

database = Database(DATABASE_URL)
engine = create_engine(DATABASE_URL)
metadata = MetaData()
