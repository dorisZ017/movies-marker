from datetime import datetime
import sqlite3

VALID_OPERATIONS = ["like", "bookmark", "rate", "review"]


def setup():
    conn, c = get_conn()
    c.execute(f"""CREATE TABLE IF NOT EXISTS movie_operations  (
                    title TEXT,
                    release_year INTEGER,
                    timestamp TEXT,
                    operation TEXT,
                    operation_input TEXT
                )""")
    conn.commit()
    conn.close()


def insert_operation(params):
    title = params.get("title")
    release_year = params.get("release_year")
    operation = params.get("operation")
    operation_input = params.get("input")

    if not title or not operation or not release_year:
        raise Exception(f"Incomplete param: {params}")

    if operation not in VALID_OPERATIONS:
        raise Exception(f"Unexpected Operation: {operation}")
    if (operation == "rate" or operation == "review") and not operation_input:
        raise Exception(f"Operation {operation} expects operation input")

    conn, c = get_conn()
    timestamp = get_timestamp()
    query = f"""INSERT INTO movie_operations 
    (title, release_year, timestamp, operation, operation_input) 
    VALUES 
    (
    "{title}", {release_year}, "{timestamp}", "{operation}", "{operation_input}"
    )""".strip()
    print(query)
    c.execute(query)
    conn.commit()
    conn.close()
    return


def get_movies(operation):
    if operation not in VALID_OPERATIONS:
        raise Exception(f"Unexpected Operation: {operation}")

    conn, c = get_conn()
    query = f"""
    SELECT * FROM movie_operations WHERE operation = "{operation}" ORDER BY timestamp DESC
""".strip()
    print(query)
    c.execute(query)
    rows = c.fetchall()

    data = []
    for row in rows:
        res = {"title": row[0], "release_year": row[1], "activity_time": row[2]}
        if operation == "rate":
            res["detail"] = row[4]
        else:
            if operation == "review":
                res["detail"] = row[4]
            else:
                res["detail"] = "NA"
        data.append(res)
    conn.close()
    return data


def get_conn():
    conn = sqlite3.connect("movie_operations.db", check_same_thread=False)
    c = conn.cursor()
    return conn, c


def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
