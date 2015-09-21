from flask import Flask, render_template, request, redirect
from flask_sockets import Sockets
import jinja2
import os
from random import choice

app = Flask(__name__)
sockets = Sockets(app)

QUOTES = ["I learned the game from William Wesley", "Back to back", "Back to back like I'm on the cover of Lethal Weapon", "Back to back like I'm Jordan '96, '97", "Whoa, very important and very pretentious", "When I look back I might be mad that I gave this attention", "Yeah, but it's weighin' heavy on my conscience", "You gon' make me step out of my fuckin' frame", "You gon' make me buy bottles for Charlamagne", "I drove here in the Wraith playin' AR-AB", "I'm not sure what it was that really made y'all mad", "But I guess this is what I gotta do to make y'all rap", "mad cause I got the midas touch", "Is that a world tour or your girl's tour?", "This ain't what she meant when she told you to open up more", "Yeah, trigger fingers turn to twitter fingers", "Make sure you hit him with the prenup", "I got the drink in me goin' back to back", "Please, check 'em for a wire or a earpiece", "Please, think before you come for the great one", "They gon' ask if I can play this shit back to back", "Runnin' through the 6 with my woes", "Countin' money you know how it goes", "Pray the real live forever man", "Pray the fakes get exposed", "I want that Ferrari then I swerve", "I want that Bugatti just to hurt", "I don't like how serious they take themselves", "I've always been me I guess I know myself", "My city too turnt up I'll take the fine for that", "Then Kanye dropped, it was polos and backpacks", "Man I'm talkin' way before hashtags", "I was runnin' through the 6 with my woes", "You know how that should go", "All I gotta do is put my mind to this shit, goddamn!", "Cancel out my ex, I put a line through that bitch", "I like all my S's with two lines through them shits", "Everybody tryna fuck you but I'm fine with that shit", "I never mind, girl that's just you", "I know you work hard for your shit", "You know they gon' hate", "Just don't play no part in that shit", "They should call me James", "Cause I'm goin' hard in this bitch", "We're just so much smarter than them", "Maybe I just needed you around me", "Drank a lot tonight, I know", "She can drive your car and you can roll", "Take you where you wanna go", "First off, I'ma start by sayin' this", "Goddamn, goddamn", "You used to call me on my cell phone", "Late night when you need my love", "Call me on my cell phone", "And I know when that hotline bling", "That can only mean one thing", "Ever since I left the city you got a reputation for yourself now", "Glasses of champagne out on the dance floor", "Hangin' with some girls I've never seen before", "Ever since I left the city, you, you, you", "Doing things I taught you gettin' nasty for someone else", "You don't need no one else", "You don't need nobody else, no"]
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
		return "Move the slider!"
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
			return "Move the slider!"
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