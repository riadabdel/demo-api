from fastapi import FastAPI
import os
import socket
import psycopg2

app = FastAPI()


def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "postgres-postgresql.demo.svc.cluster.local"),
        database=os.getenv("DB_NAME", "postgres"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres")
    )


@app.get("/")
def home():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS visits (
            id SERIAL PRIMARY KEY,
            count INTEGER
        )
        """
    )

    cur.execute("SELECT count FROM visits WHERE id=1;")
    row = cur.fetchone()

    if row:
        count = row[0] + 1
        cur.execute(
            "UPDATE visits SET count=%s WHERE id=1;",
            (count,)
        )
    else:
        count = 1
        cur.execute(
            "INSERT INTO visits(id, count) VALUES(1, 1);"
        )

    conn.commit()
    cur.close()
    conn.close()

    return {
        "application": "Kubernetes Demo",
        "version": "v7",
        "pod": socket.gethostname(),
        "database": "connected",
        "visits": count
    }
