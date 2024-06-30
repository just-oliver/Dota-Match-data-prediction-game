import streamlit as st
import pandas as pd
import psycopg2 as psql


conn = psql.connect(database = 'pagila',
                    user = st.secrets["sql_user"],
                    host = st.secrets["host"],
                    password = st.secrets["sql_password"],
                    port=5432
                    )

cur = conn.cursor()

query_sql = '''
            SELECT
                *
            FROM
                student.ojdb_matches
            OFFSET
            LIMIT 1;
'''

cur.execute(query_sql)

row = cur.fetchone()


st.markdown(f"## :red[Match ID : {row[0]}]")
