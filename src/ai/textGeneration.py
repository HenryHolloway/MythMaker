import aiohttp
import asyncio
import requests
import json

async def sendMessageAndStreamResponse(conversation: dict, messageCallback: callable) -> bool:
	"""
	Send a message and stream the response from the AI model.

	This function sends a conversation history to an AI model endpoint and streams
	the response back. It invokes a callback function for each part of the response
	received.

	Args:
		conversation (dict): The conversation history to send to the AI model.
		messageCallback (function): A callback function to handle each part of the 
									response. It should accept three arguments: 
									sender (str), message (str), and done (bool).

	Returns:
		bool: True if the response is fully received and marked as done, False otherwise.
	"""
	print("Send & stream called.")
	# Simulation of constructing a payload with the entire conversation history
	payload = {
		"model": "mannix/llama3.1-8b-abliterated:latest",
		"messages": conversation,  # Use provided conversation history
		"options": {
			"num_gpu": 0
		}
	}

	print("Payload: ", payload)

	# Assuming your ollama endpoint and providing it with the full conversation
	async with aiohttp.ClientSession() as session:
		async with session.post('http://localhost:11434/api/chat', json=payload) as response:
			# Assuming the response is a stream of JSON objects
			async for line in response.content:
				if line.strip():  # Filter out keep-alive chunks
					decodedLine = json.loads(line.decode('utf-8'))
					message = decodedLine.get('message', {})
					print(message)
					if message:
						# Invoke the callback for each received part of the response
						messageCallback("assistant", message['content'], decodedLine.get('done'))

					if decodedLine.get('done'):
						return True

	return False


def sendMessageAndStaticResponse(conversation: dict, json: bool = False) -> bool:
	"""
	Send a message and get a static response from the AI model.

	This function sends a conversation history to an AI model endpoint and retrieves
	a static response. The response is not streamed but received as a whole.

	Args:
		conversation (dict): The conversation history to send to the AI model.
		json (bool): If True, the response will be formatted as JSON.

	Returns:
		bool or dict: The response message if successful, otherwise False.
	"""
	print("Send & static called.")
	# Simulation of constructing a payload with the entire conversation history
	payload = {
		"model": "mannix/llama3.1-8b-abliterated:latest",
		"messages": conversation,
		"options": {
			"num_gpu": 0
		},
		"stream": False
	}

	if json:
		payload["format"] = "json"

	print("Payload: ", payload)

	response = requests.post("http://localhost:11434/api/chat", json=payload)
	if response.status_code == 200:
		responseData = response.json()
		print("Response: ", responseData)
		print(responseData.get("done"))
		if responseData.get("done"):
			return responseData.get("message")
	else:
		print("Failed to get response from the server.")
		return False


#def test_sendMessageAndStaticResponse():
def testSendMessageAndStaticResponse():
	conversation = [{"role": "user", "content": "Hi, how are you?"}]

	# This line directly calls the function with the provided inputs.
	print("Returned from send massage: ", sendMessageAndStaticResponse(conversation))


#async def test_sendMessageAndStreamResponse():
async def testSendMessageAndStreamResponse():
	conversation = [{"role": "user", "content": "Hi, how are you?"}]

	def messageCallback(sender, message, done):
		# Adapt this function to log or print the message information to validate the behavior
		print(f"Received message from {sender} with content '{message}'")

	# This line directly calls the function with the provided inputs.
	await sendMessageAndStreamResponse(conversation, messageCallback)


if __name__ == "__main__":
	asyncio.run(testSendMessageAndStreamResponse())
	#testSendMessageAndStaticResponse()
