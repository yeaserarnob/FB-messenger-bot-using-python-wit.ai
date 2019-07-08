from wit import Wit 

wit_access_token = "I6ZCACAOQFZSAA2WUYBWPMGET2CKMQFM"
client = Wit(access_token = wit_access_token)

def wit_response(message_text):
	resp = client.message(message_text)
	
	entity = None
	value = None

	try:
		entity = list(resp['entities'])[0]
		value = resp['entities'][entity][0]['value']
	except:
		pass

	return (entity, value)

# print(wit_response("I want sports news"))