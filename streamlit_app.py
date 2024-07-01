import streamlit as st
import pandas as pd
import psycopg2 as psql
import json

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
match_id = row[0]
st.markdown(f"## :red[Match ID : {match_id}]")
## Get heroes
hero_sql = f'''
            SELECT *
            FROM student.ojdb_hero_picks
            WHERE match_id = {match_id}
            ORDER BY team ASC;
'''
cur.execute(hero_sql)
hero_rows = cur.fetchall()
hero_ids = [str(hero_row[1]) for hero_row in hero_rows]

with open('data/heroes.json', 'r') as f:
    hero_id_dict = json.load(f)


items_ids = [hero_row[4] for hero_row in hero_rows]
# int to str
items_ids = [[str(x) for x in item_ids] for item_ids in items_ids]


with open('data/item_ids.json', 'r') as f:
    item_id_dict = json.load(f)
items = [[item_id_dict[x] for x in item_ids] for item_ids in items_ids]

with open('data/items.json', 'r') as f:
    item_dict = json.load(f)



items_details = [[(item_dict[item]['dname'],item_dict[item]['img']) for item in item_list if item ] for item_list in items]

hero_details = [(hero_id_dict[hero_id]['localized_name'], hero_id_dict[hero_id]['img']) for hero_id in hero_ids]


cols = st.columns(2)
with cols[0]:
    st.header(':green[Radiant Team]')
    for i, hero in enumerate(hero_details[:5]):
        st.image('https://cdn.cloudflare.steamstatic.com/' + hero[1], caption=hero[0])
        st.markdown('Items')
        item_cols = st.columns(3)
        items = items_details[i]
        for j,item in enumerate(items):
            with item_cols[j%3]:
                if items[j][1] == 'empty':
                    st.image('./images/empty.png', caption=items[j][0],width=88)
                else:
                    if len(items[j][0]) > 12:
                        st.image('https://cdn.cloudflare.steamstatic.com/'+items[j][1], caption=items[j][0][:13])
                    else:
                        st.image('https://cdn.cloudflare.steamstatic.com/'+items[j][1], caption=items[j][0])


with cols[1]:
    st.header(':red[Dire Team]')
    for i, hero in enumerate(hero_details[5:]):
        i = i + 5
        st.image('https://cdn.cloudflare.steamstatic.com/' + hero[1], caption=hero[0],)
        st.markdown('Items')
        item_cols = st.columns(3)
        items = items_details[i]
        for j,item in enumerate(items):
            with item_cols[j%3]:
                if items[j][1] == 'empty':
                    st.image('./images/empty.png', caption=items[j][0],width=88)
                else:
                    if len(items[j][0]) > 12:
                        st.image('https://cdn.cloudflare.steamstatic.com/'+items[j][1], caption=items[j][0][:13])
                    else:
                        st.image('https://cdn.cloudflare.steamstatic.com/'+items[j][1], caption=items[j][0])
## Choice Form
with st.form('Player Guess'):
    st.markdown('**Predict which team will win!**')
    selection = st.radio('Team:', ['Radiant','Dire'])
    submition_button = st.form_submit_button()

if submition_button:
    if selection == 'Radiant':
        st.markdown(f'You have guessed the **:green[Radiant]** team will win!')
    else:
        st.markdown(f'You have guessed the **:red[Dire]** team will win!')