from flask import Flask, render_template, request, redirect
from flask_sockets import Sockets
import jinja2
import os
from random import choice

app = Flask(__name__)
sockets = Sockets(app)

BACK_TO_BACK = ["But I guess this is what I gotta do to make y'all rAp", "Yeah, I learned the game from William Wesley", "Back to back like I'm on the cover of Lethal Weapon", "Back to back like I'm Jordan '96, '97", "Whoa, very important and very pretentious", "When I look back I might be mad that I gave this attention", "Yeah, but it's weighin' heavy on my conscience", "You gon' make me buy bottles for Charlamagne", "I drove here in the Wraith playin' AR-AB", "I'm not sure what it was that really made y'all mad", "But I guess this is what I gotta do to make y'all rap", "This for y'all that think that I don't write enough", "They just mad cause I got the midas touch", "Is that a world tour or your girl's tour?", "I know that you gotta be a thug for her", "This ain't what she meant when she told you to open up more", "Yeah, trigger fingers turn to twitter fingers", "Make sure you hit him with the prenup", "I got the drink in me goin' back to back", "Yeah, goin' back to back", "I don't wanna hear about this ever again", "Not even when she tell him that they better as friends", "I didn't wanna do it, gave me every reason", "Please, check 'em for a wire or a earpiece", "Please, think before you come for the great one", "I'm talkin' boasy and gwanin wassy", "They gon' ask if I can play this shit back to back", "Yeah, they want it back to back", "I took a break from Views, now it's back to that"]
QUOTES = BACK_TO_BACK
QUOTES_MAP = {}

def map_quotes():
	for i in QUOTES:
		current_char_count = len(i)
		if QUOTES_MAP.get(current_char_count) is not None:
			x = QUOTES_MAP[current_char_count]
			x.append(i)
			QUOTES_MAP[current_char_count] = x
		else:
			QUOTES_MAP[current_char_count] = [i]

def get_quote(num):
	try:
		num = int(num)
	except:
		return "Coudnt find any :("
	quote_list = None
	delta = 0
	while quote_list is None:
		if delta == 0:
			quote_list = QUOTES_MAP.get(num)
			delta += 1
			continue
		if delta + num < longest_quote_length():
			quote_list = QUOTES_MAP.get(num + delta)
		if quote_list is None and num - delta > shortest_quote_length():
			quote_list = QUOTES_MAP.get(num - delta)
		delta += 1
		if delta + num > longest_quote_length() and num - delta < shortest_quote_length():
			return "Couldnt find any :("
	# quote_list = QUOTES_MAP.get(num)
	if quote_list is None:
		return ""
	return choice(quote_list)

def shortest_quote_length():
	return min(map(len, QUOTES))

def longest_quote_length():
	return max(map(len, QUOTES))

@app.route('/')
def index():
	return render_template("index.html", shortest=shortest_quote_length(), longest=longest_quote_length())

@sockets.route('/echo')
def echo_socket(ws):
    while True:
        message = ws.receive()
        ws.send(str(get_quote(message)))

@app.route('/character-count', methods=['GET', 'POST'])
def character_count():
	return str(len(QUOTES)) + "  " + str(QUOTES_MAP)
	characters = request.args.get('characters')
	try:
		characters = int(characters)
	except:
		return "Error!"
	return str(characters) + " characters: "

if __name__ == '__main__':
	# port = int(os.environ.get('PORT', 8000))
	# app.run(host='0.0.0.0', port=port,debug=True)
	map_quotes()
	from gevent import pywsgi
	from geventwebsocket.handler import WebSocketHandler
	server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
	server.serve_forever()