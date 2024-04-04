import pandas as pd
from sqlalchemy import create_engine

def import_json_data(json_file, table_name):
    from app import db 

    df = pd.read_json(json_file)
    engine = create_engine(db.engine.url)
    df.to_sql(table_name, engine, if_exists='replace', index=False)
    print("Data imported successfully into database table")
