from flask import Flask, render_template, request, redirect  
import wordsLogic
import random

from wordsLogic import creds
from DBcm import UseDatabase

app = Flask(__name__)


#function to generate word 
def generate_large_word(filepath="static/words-huge"):
    """Generates a random word with 8 or more letters from the dictionary file."""
    try:
        with open(filepath, "r") as file:
            words = [line.strip() for line in file if len(line.strip()) >= 8]
        return random.choice(words) if words else None
    except FileNotFoundError:
        print(f"Error: The file '{filepath}' was not found.")
        return None


#routes
@app.get("/")
def hello():
    return render_template(
                "index.html",
                the_title="Welcome to words 4",
    )

@app.get("/opening")
def show_opening_screen():
    return render_template("index.html", the_title="Welcome to Words 4")

         
@app.route('/play',methods=['GET'])
def show_play_screen():
	sourceword = generate_large_word()
	return render_template("play.html", the_title="Play word game 4", sourceword=sourceword)


@app.post("/process")
def process():
    who = request.form.get('name')
    sourceword = request.form.get('sourceword')
    matches = request.form.get('4words', '').strip()
    time_taken = float(request.form.get('time_taken'))
    win_fail = 'Win' if len(matches.split()) == 7 else 'Fail'
    ip_address = request.remote_addr
    user_agent = request.headers.get('User-Agent')

    #Insert game attempt into the log table
    with UseDatabase(creds) as cursor:
        cursor.execute("""
            INSERT INTO log (who, sourceword, matches, win_fail, time_taken, ip_address, user_agent)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (who, sourceword, matches, win_fail, time_taken, ip_address, user_agent))

        #If the game is a win, check leaderboard qualify?
        if win_fail == 'Win':
            cursor.execute("SELECT COUNT(*) FROM topten")
            count = cursor.fetchone()[0]

            if count < 10:
                cursor.execute("""
                    INSERT INTO topten (time_taken, who, sourceword, matches, win_fail)
                    VALUES (%s, %s, %s, %s, %s)
                """, (time_taken, who, sourceword, matches, win_fail))
            else:
                cursor.execute("SELECT MAX(time_taken) FROM topten")
                max_time = cursor.fetchone()[0]
                if time_taken < max_time:
                    cursor.execute("DELETE FROM topten WHERE time_taken = %s LIMIT 1", (max_time,))
                    cursor.execute("""
                        INSERT INTO topten (time_taken, who, sourceword, matches, win_fail)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (time_taken, who, sourceword, matches, win_fail))

            #Update positions based on time_taken
            cursor.execute("SET @rank = 0;")
            cursor.execute("""
                UPDATE topten
                SET position = (@rank := @rank + 1)
                ORDER BY time_taken ASC;
            """)


    #Redirect to pass or fail page
    if win_fail == 'Win':
        return render_template('pass.html', time_taken=time_taken)
    else:
        return render_template('fail.html', time_taken=time_taken)


@app.route('/pass')
def pass_page():
    	return render_template('pass.html')


@app.route('/fail')
def fail_page():
	return render_template('fail.html')

@app.route('/top10')
def top_ten():
    with UseDatabase(creds) as cursor:
        # Retrieve the top ten players ordered by their time_taken (ascending)
        cursor.execute("""
            SELECT position, time_taken, who, sourceword, matches
            FROM topten
            ORDER BY position ASC
            LIMIT 10
        """)
        top_ten_results = cursor.fetchall()  # Fetch all rows

    return render_template("topten.html",the_title="Top 10 Scores", results=top_ten_results)



    
@app.route('/log')
def show_log():
    with UseDatabase(creds) as cursor:
        # Query to fetch the relevant columns from the log table
        cursor.execute("""
            SELECT win_fail, sourceword, timestamp, ip_address, user_agent, matches
            FROM log
            ORDER BY timestamp DESC
        """)
        log_entries = cursor.fetchall()  # Fetch all rows

    # Pass the fetched data to the log.html template
    return render_template("log.html", the_title="Logged Information", logs=log_entries)


if __name__ == "__main__":
    app.run(debug=True)
