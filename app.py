from flask import Flask, render_template, request, redirect
import jinja2
import os

app = Flask(__name__)

BACK_TO_BACK = ["Yeah, I learned the game from William Wesley", "Back to back like I'm on the cover of Lethal Weapon", "Back to back like I'm Jordan '96, '97", "Whoa, very important and very pretentious", "When I look back I might be mad that I gave this attention", "Yeah, but it's weighin' heavy on my conscience", "You gon' make me buy bottles for Charlamagne", "I drove here in the Wraith playin' AR-AB", "I'm not sure what it was that really made y'all mad", "But I guess this is what I gotta do to make y'all rap", "This for y'all that think that I don't write enough", "They just mad cause I got the midas touch", "Is that a world tour or your girl's tour?", "I know that you gotta be a thug for her", "This ain't what she meant when she told you to open up more", "Yeah, trigger fingers turn to twitter fingers", "Make sure you hit him with the prenup", "I got the drink in me goin' back to back", "Yeah, goin' back to back", "I don't wanna hear about this ever again", "Not even when she tell him that they better as friends", "I didn't wanna do it, gave me every reason", "Please, check 'em for a wire or a earpiece", "Please, think before you come for the great one", "I'm talkin' boasy and gwanin wassy", "They gon' ask if I can play this shit back to back", "Yeah, they want it back to back", "I took a break from Views, now it's back to that"]
QUOTES = BACK_TO_BACK

def count_words(s):
	return len(s.split(" "))

def shortest_quote_length():
	return min(map(count_words, QUOTES))

def longest_quote_length():
	return max(map(count_words, QUOTES))

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/word-count', methods=['GET', 'POST'])
def word_count():
	words = request.args.get('words')
	try:
		words = int(words)
	except:
		return "Error!"
	return str(words) + " words: " + str(shortest_quote_length()) + "-" + str(longest_quote_length())

if __name__ == '__main__':
	port = int(os.environ.get('PORT', 8000))
	app.run(host='0.0.0.0', port=port,debug=True)