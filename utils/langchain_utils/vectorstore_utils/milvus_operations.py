from pymilvus import Collection, MilvusException, connections, db, utility


def find_or_create_database(milvus_host: str, milvus_port:int,  token: str, db_name: str):
    _conn = connections.connect(host=milvus_host, port=milvus_port, token=token)

    # Check if the database exists, else creaate
    try:
        existing_databases = db.list_database()
        if db_name in existing_databases:
            print(f"Database '{db_name}' already exists.")
        else:
            print(f"Database '{db_name}' does not exist.")
            _database = db.create_database(db_name)
            print(f"Database '{db_name}' created successfully.")
    except MilvusException as e:
        print(f"An error occurred: {e}")