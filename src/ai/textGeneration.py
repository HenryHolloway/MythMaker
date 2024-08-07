import aiohttp
import asyncio
import requests
import json

async def send_message_and_stream_response(conversation, message_callback):
    print("Send & stream called.")
    # Simulation of constructing a payload with the entire conversation history
    payload = {
        "model": "internlm2:latest",
        "messages": conversation,  # Use provided conversation history
    }

    print("Payload: " , payload)

    # Assuming your ollama endpoint and providing it with the full conversation
    async with aiohttp.ClientSession() as session:
        async with session.post('http://localhost:11434/api/chat', json=payload) as response:
            # Assuming the response is a stream of JSON objects
            async for line in response.content:
                if line.strip():  # Filter out keep-alive chunks
                    decoded_line = json.loads(line.decode('utf-8'))
                    message = decoded_line.get('message', {})
                    print(message)
                    if message:
                        # Invoke the callback for each received part of the response
                        message_callback("assistant", message['content'], decoded_line.get('done'))

                    if decoded_line.get('done'):
                        break



def send_message_and_static_response(conversation, json=False):
    print("Send & static called.")
    # Simulation of constructing a payload with the entire conversation history
    payload = {
        "model": "internlm2:latest",
        "messages": conversation,
        "stream": False
    }

    if json:
        payload["format"] = "json"

    print("Payload: ", payload)

    response = requests.post("http://localhost:11434/api/chat", json=payload)
    if response.status_code == 200:
        response_data = response.json()
        print("Response: ", response_data)
        print(response_data.get("done"))
        if response_data.get("done"):
            return response_data.get("message")
    else:
        print("Failed to get response from the server.")
        return False





def test_send_message_and_static_response():
    conversation = [{"role": "user", "content": "Why is the sky blue?"}]

    # This line directly calls the function with the provided inputs.
    print("Returned from send massage: ", send_message_and_static_response(conversation))

async def test_send_message_and_stream_response():
    conversation = [{"role": "user", "content": "Hi, how are you?"}]

    def message_callback(sender, message):
        # Adapt this function to log or print the message information to validate the behavior
        print(f"Received message from {sender} with content '{message}'")

    # This line directly calls the function with the provided inputs.
    await send_message_and_stream_response(conversation, message_callback)


if __name__ == "__main__":
    #asyncio.run(test_send_message_and_stream_response())
    test_send_message_and_static_response()

