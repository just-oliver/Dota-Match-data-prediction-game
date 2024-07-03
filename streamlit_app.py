import streamlit as st
import pandas as pd
import psycopg2 as psql
import json
import plotly.graph_objects as go

st.title('Dota 2 Match Guessing Game')

if 'score' not in st.session_state:
    st.session_state.score = 0


st.header(f"Score: {st.session_state.score}")


rank = st.selectbox('Rank of Game', ['Herald',
                                     'Guardian',
                                     'Crusader',
                                     'Archon',
                                     'Legend',
                                     'Ancient',
                                     'Divine',
                                     'Immortal'])

st.divider()
st.markdown("<h2 style='text-align: center;'>Hero Picks</h2>", unsafe_allow_html=True)


# check box to show items
see_items = st.checkbox(f'Show Items')
see_neutral = st.checkbox(f'Show Neutral Item')
see_backpack = st.checkbox(f'Show Backpack')

#
rank_dists = {'Herald':(10,15),
            'Guardian':(20,25),
            'Crusader':(30,35),
            'Archon':(40,45),
            'Legend':(50,55),
            'Ancient':(60,65),
            'Divine':(70,75),
            'Immortal':(80,85)}

dist = rank_dists[rank]

conn = psql.connect(database = 'pagila',
                    user = st.secrets["sql_user"],
                    host = st.secrets["host"],
                    password = st.secrets["sql_password"],
                    port=5432
                    )

cur = conn.cursor()



@st.cache_data
def match_selection(dist):
    '''
    Creating a function here to cache the matchid and outcome 
    to prevent the form submission from over writing the previous match
    '''
    conn = psql.connect(database = 'pagila',
                    user = st.secrets["sql_user"],
                    host = st.secrets["host"],
                    password = st.secrets["sql_password"],
                    port=5432
                    )

    cur = conn.cursor()
    

    

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
    radiant_wins = row[2]
    return match_id, radiant_wins

match_id, radiant_wins = match_selection(dist)
## Page Start


## Get heroes
hero_sql = f'''
            SELECT *
            FROM student.ojdb_hero_picks
            WHERE match_id = {match_id}
            ORDER BY team ASC, net_worth DESC; -- gets the radiant heroes first followed by dire, then top networth heroes
'''
cur.execute(hero_sql)
hero_rows = cur.fetchall()
hero_ids = [str(hero_row[1]) for hero_row in hero_rows]
facets = [hero_row[3] for hero_row in hero_rows]

# Getting hero names and image locations from json
with open('data/heroes.json', 'r') as f:
    hero_id_dict = json.load(f)

# get facet name
with open('data/hero_abilities.json', 'r') as f:
    hero_abilities_dict = json.load(f)

hero_abilities_name = [hero_id_dict[hero_id]['name'] for hero_id in hero_ids]
facet_names = []

for i,facet in enumerate(facets):
    facet_names.append(hero_abilities_dict[hero_abilities_name[i]]['facets'][facet-1]['title'])
    
hero_details = [(hero_id_dict[hero_id]['localized_name'], hero_id_dict[hero_id]['img']) for hero_id in hero_ids]

items_ids = [hero_row[4] for hero_row in hero_rows]
backpacks_ids = [hero_row[5] for hero_row in hero_rows]
neutrals_ids = [str(hero_row[6]) for hero_row in hero_rows]
networths = [hero_row[13] for hero_row in hero_rows]






# int to str
items_ids = [[str(x) for x in item_ids] for item_ids in items_ids]
backpacks_ids = [[str(x) for x in backpack_ids] for backpack_ids in backpacks_ids]


with open('data/item_ids.json', 'r') as f:
    item_id_dict = json.load(f)

items = [[item_id_dict[x] for x in item_ids] for item_ids in items_ids]
backpacks = [[item_id_dict[x] for x in backpack_ids] for backpack_ids in backpacks_ids]
neutrals = [item_id_dict[neutral_id] for neutral_id in neutrals_ids]



with open('data/items.json', 'r') as f:
    item_dict = json.load(f)

items_details = [[(item_dict[item]['dname'],item_dict[item]['img']) for item in item_list] for item_list in items]
backpacks_details = [[(item_dict[item]['dname'],item_dict[item]['img']) for item in backpack_list] for backpack_list in backpacks]
neutrals_details = [(item_dict[neutral]['dname'], item_dict[neutral]['img']) for neutral in neutrals]



cols = st.columns(2)
with cols[0]:
    st.header(':green[Radiant Team]')
    for i, hero in enumerate(hero_details[:5]):
        if len(f"{hero[0]} ({facet_names[i]})") > 27:
            st.image('https://cdn.cloudflare.steamstatic.com/' + hero[1], caption=f"{hero[0]} ({facet_names[i]})"[:25] + '...', width=200)
        else:
            st.image('https://cdn.cloudflare.steamstatic.com/' + hero[1], caption=f"{hero[0]} ({facet_names[i]})", width=200)
        if see_items:
            st.markdown(f"{hero[0]}'s Items")
            item_cols = st.columns(3)
            items = items_details[i]
            for j,item in enumerate(items):
                with item_cols[j%3]:
                    if item[1] == 'empty':
                        st.image('./images/empty.png', caption=item[0],width=88)
                    else:
                        if len(item[0]) > 12:
                            st.image('https://cdn.cloudflare.steamstatic.com/'+item[1], caption=item[0][:11] + '...')
                        else:
                            st.image('https://cdn.cloudflare.steamstatic.com/'+item[1], caption=item[0])
        if see_neutral:
            st.markdown(f"{hero[0]}'s Neutral Item")
            neutral = neutrals_details[i]
            if neutral[1] == 'empty':
                st.image('./images/empty.png', caption=neutral[0],width=88)
            else:
                if len(neutral[0]) > 12:
                    st.image('https://cdn.cloudflare.steamstatic.com'+neutral[1], caption=neutral[0][:11] + '...')
                else:
                    st.image('https://cdn.cloudflare.steamstatic.com'+neutral[1], caption=neutral[0])
        if see_backpack:
            st.markdown(f"{hero[0]}'s Backpack")
            backpack_cols = st.columns(3)
            backpacks = backpacks_details[i]
            for j,item in enumerate(backpacks):
                with backpack_cols[j%3]:
                    if item[1] == 'empty':
                        st.image('./images/empty.png', caption=item[0],width=88)
                    else:
                        if len(item[0]) > 12:
                            st.image('https://cdn.cloudflare.steamstatic.com'+item[1], caption=item[0][:11] + '...')
                        else:
                            st.image('https://cdn.cloudflare.steamstatic.com'+item[1], caption=item[0])
        



with cols[1]:
    st.header(':red[Dire Team]')
    for i, hero in enumerate(hero_details[5:]):
        i = i + 5
        if len(f"{hero[0]} ({facet_names[i]})") > 27:
            st.image('https://cdn.cloudflare.steamstatic.com/' + hero[1], caption=f"{hero[0]} ({facet_names[i]})"[:25] + '...', width=200)
        else:
            st.image('https://cdn.cloudflare.steamstatic.com/' + hero[1], caption=f"{hero[0]} ({facet_names[i]})", width=200)
        if see_items:
            st.markdown(f"{hero[0]}'s Items")
            item_cols = st.columns(3)
            items = items_details[i]
            for j,item in enumerate(items):
                with item_cols[j%3]:
                    if items[j][1] == 'empty':
                        st.image('./images/empty.png', caption=items[j][0],width=88)
                    else:
                        if len(items[j][0]) > 12:
                            st.image('https://cdn.cloudflare.steamstatic.com/'+items[j][1], caption=items[j][0][:11] + '...')
                        else:
                            st.image('https://cdn.cloudflare.steamstatic.com/'+items[j][1], caption=items[j][0])
        if see_neutral:
            st.markdown(f"{hero[0]}'s Neutral Item")
            neutral = neutrals_details[i]
            if neutral[1] == 'empty':
                st.image('./images/empty.png', caption=neutral[0],width=88)
            else:
                if len(neutral[0]) > 12:
                    st.image('https://cdn.cloudflare.steamstatic.com'+neutral[1], caption=neutral[0][:11] + '...')
                else:
                    st.image('https://cdn.cloudflare.steamstatic.com'+neutral[1], caption=neutral[0])
        if see_backpack:
            st.markdown(f"{hero[0]}'s Backpack")
            backpack_cols = st.columns(3)
            backpacks = backpacks_details[i]
            for j,item in enumerate(backpacks):
                with backpack_cols[j%3]:
                    if item[1] == 'empty':
                        st.image('./images/empty.png', caption=item[0],width=88)
                    else:
                        if len(item[0]) > 12:
                            st.image('https://cdn.cloudflare.steamstatic.com'+item[1], caption=item[0][:11] + '...')
                        else:
                            st.image('https://cdn.cloudflare.steamstatic.com'+item[1], caption=item[0])
        


st.divider()
st.markdown("<h2 style='text-align: center;'>Game Statistics</h2>", unsafe_allow_html=True)
## Networth barplot
hero_names = [hero_detail[0] for hero_detail in hero_details]
side = ["radiant" if i < 5 else "dire" for i in range(10)]
combined = list(zip(networths, hero_names, side))
combined.sort(reverse=True, key=lambda index:index[0])
sorted_networths = [entry[0] for entry in combined]
sorted_names = [entry[1] for entry in combined]
sorted_sides = [entry[2] for entry in combined]
colours = ['green' if side == 'radiant' else 'red' for side in sorted_sides]

fig_networth = go.Figure(data=[go.Bar(
    x=sorted_names,
    y=sorted_networths,
    marker_color=colours,
    text=sorted_networths,
    textposition='outside'
)])


st.plotly_chart(fig_networth)
## level barplot


st.divider()
## Choice Form
form_placeholder = st.empty()
with form_placeholder.form('Player Guess'):
    st.markdown('**Predict which team will win!**')
    selection = st.radio('Team:', ['Radiant','Dire'])
    submition_button = st.form_submit_button()


if submition_button:
    form_placeholder.empty()
    if (radiant_wins and selection == 'Radiant') or  (not radiant_wins and selection == 'Dire'):
        st.markdown(f'### You have Guessed {selection} correctly and gained **100 points**! 🙌')
        st.session_state.score += 100
        st.balloons()
        
    else:
        st.markdown(f'### You have Guessed {selection} incorrectly and lose **100 points**! 👎')
        st.session_state.score -= 100
    st.markdown(f"## [:red[Match ID : {match_id}]](https://www.dotabuff.com/matches/{match_id})")

if st.button("New Game"):
        st.cache_data.clear()
        st.rerun()