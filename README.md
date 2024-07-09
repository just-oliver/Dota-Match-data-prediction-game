# ⚖ Dota Match data & prediction game


<a href="https://dota-match-data-ma5ywyzq3xa.streamlit.app/">
  <img src="https://upload.wikimedia.org/wikipedia/commons/b/b8/Dota-2-simplified-logo.svg" alt="Open in Streamlit" width="40" height="40">
  <figcaption>view app on Streamlit Cloud</figcaption>
</a>

## Inspiration & Methodology
Inspired by guessing games such as wordle and heardle, where information is gradually given to the user to aid the player at the cost of a final score.<br>
Since Dota is a game of many kind of resources which can be visualised such as gold, items, experience and hero picks. 
My plan was to give the player first the hero picks of a random public ranked game played in DOTA 2.
The player has then 6 options of reveling more data regarding specific hero picks including items and gold per minuite metrics for a cost of -10 off the final score.
3 more advanced indicators priced at -35, showing highly corrolated information with team victory such as the distributed net worths of each hero.

To create this application I used the OpenDota API to harvest public match data and benchmark metrics which I then transformed and stored in a private PostgreSQL tables.
Then the frontend and application logic I created in Streamlit due to the simplified nature to spin up data based applications quickly in the browser.

While DOTA is a great game it can often put off new players due to it's steep learning curve and often unfriendly learning environment.
I hope this app can champion a safe learning space for new players to get a deeper understanding of how hero picks and resources contribute to victory within the game.

## Progression and Further Ambitions
To progress this app further I will ammend the following changes
1. Create an account system so that scores may persist between sessions
2. Rebalance the penalty of each of the indicators available to represent their overall significance more accurately
3. Create a random forests classifier to predict which team is likely to win based on the data given to the user - this can be used to scale the 'betting odds'

### How to run it on your own machine

1. Install the requirements

   ```
   $ pip install -r requirements.txt
   ```

2. Run the app

   ```
   $ streamlit run streamlit_app.py
   ```
