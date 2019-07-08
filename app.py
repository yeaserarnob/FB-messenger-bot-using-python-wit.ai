import os, sys
from flask import Flask, request
from utils import wit_response
from pymessenger import Bot

app = Flask(__name__)

PAGE_ACCESS_TOKEN = "EAAGDF48UrOYBAKwhnHKq3lBrZAVSEj5SgvVnQ9kH2LoyJZC781RcEAxXD0DYHcJd5qX65C2AlamCeGOvF7hyR7XVZBye1LzcyyNLV4GwZCUFO6wau3GatMkqEVG4nnzgWmiORdap7FLBJOe02PJCxQpULCLejl2qnwxkcwZCtbSB9ZAb8pqApYROHuKt6BN0MZD"

bot = Bot(PAGE_ACCESS_TOKEN)

@app.route('/', methods=['GET'])
def verify():
	# Webhook verification
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "hello":
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello world", 200

@app.route('/', methods=['POST'])
def webhook():
	data = request.get_json()
	print(data)

	if data['object'] == 'page':
		for entry in data['entry']:
			for messaging_event in entry['messaging']:
				sender_id = messaging_event['sender']['id']
				# recipient_id = messaging_event['recipient']['id']

				if messaging_event.get('message'):
					if 'text' in messaging_event['message']:
						messaging_text = messaging_event['message']['text']
					else:
						messaging_text = 'no text'
					
					response = None

					entity, value = wit_response(messaging_text)

					if entity == 'newstype':
						response =  "Ok. I will send you {} news".format(str(value))
					elif entity == 'locationn':
						response = "Ok. So, you live in {0}. I will send you top headlines about {0}".format(str(value))
					elif entity == 'hello':
						response = "Hello there".format(str(value))

					if response == None:
						response = "Sorry, I didn't understand !"

					bot.send_text_message(sender_id, response)

	return "ok", 200



def log(message):
	print(message)
	sys.stdout.flush()


if __name__ == "__main__":
	app.run(debug = True, port = 80)