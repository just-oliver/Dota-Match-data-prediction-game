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

rank = st.selectbox('Rank of Game', ['Herald',
                                     'Guardian',
                                     'Crusader',
                                     'Archon',
                                     'Legend',
                                     'Ancient',
                                     'Divine',
                                     'Immortal'])

rank_dists = {'Herald':(10,15),
            'Guardian':(20,25),
            'Crusader':(30,35),
            'Archon':(40,45),
            'Legend':(50,55),
            'Ancient':(60,65),
            'Divine':(70,75),
            'Immortal':(80,85)}

dist = rank_dists[rank]

query_sql = f'''
            SELECT *
            FROM student.ojdb_matches
            WHERE avg_rank BETWEEN {dist[0]} AND {dist[1]}
            ORDER BY RANDOM()
            LIMIT 1
'''

cur.execute(query_sql)

row = cur.fetchone()


st.markdown(f"## :red[Match ID : {row[0]}]")

with st.form('Player Guess'):
    st.markdown('**Predict which team will win!**')
    selection = st.radio('Team:', ['Radiant','Dire'])
    submition_button = st.form_submit_button()

if submition_button:
    if selection == 'Radiant':
        st.markdown(f'You have guessed the **:green[Radiant]** team will win!')
    else:
        st.markdown(f'You have guessed the **:red[Dire]** team will win!')