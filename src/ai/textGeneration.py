import aiohttp
import asyncio
import json

async def send_message_and_stream_response(conversation, message_callback):
    # Simulation of constructing a payload with the entire conversation history
    payload = {
        "model": "openchat",
        "messages": conversation,  # Use provided conversation history
    }

    # Assuming your ollama endpoint and providing it with the full conversation
    async with aiohttp.ClientSession() as session:
        async with session.post('http://localhost:11434/api/chat', json=payload) as response:
            # Assuming the response is a stream of JSON objects
            async for line in response.content:
                if line.strip():  # Filter out keep-alive chunks
                    decoded_line = json.loads(line.decode('utf-8'))
                    message = decoded_line.get('message', {})
                    if message:
                        # Invoke the callback for each received part of the response
                        message_callback("AI", message['content'], "#EEEEEE")

                    if decoded_line.get('done'):
                        break


async def test_send_message_and_stream_response():
    conversation = [{"role": "user", "content": "Hi, how are you?"}]

    def message_callback(sender, message, color):
        # Adapt this function to log or print the message information to validate the behavior
        print(f"Received message from {sender} with content '{message}' and color {color}")

    # This line directly calls the function with the provided inputs.
    await send_message_and_stream_response(conversation, message_callback)

if __name__ == "__main__":
    asyncio.run(test_send_message_and_stream_response())