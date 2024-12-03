from flask import Flask, render_template, request  
import 4words

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
	the_pattern = request.form["4words"]
	the_results = 4words.validate_wordlist(sourceword, the_pattern)
	return the_results
	

    
@app.get("/top10")
def show_top10():
        return render_template("top10.html", the_title="Leaderboard")
        
@app.get("/log")
def show_log():
        return render_template("log.html", the_title="Log")
    


if __name__ == "__main__":
    app.run(debug=True)
