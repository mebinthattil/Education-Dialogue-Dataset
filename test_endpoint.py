from sagemaker.predictor import retrieve_default

endpoint_name = "jumpstart-dft-meta-textgeneration-l-20250608-030122"
predictor = retrieve_default(endpoint_name)

system_prompt = "You are a teacher teaching 5 year old kids. You answer questions in a polite manner. Do not repeat yourself. You have to simplify concepts and explain so that even a 5 year old can understand."
conversation_history = f"system: {system_prompt}\n"

while True:
    user_message = input("You: ").strip()
    if user_message.lower() in {"exit", "quit"}:
        break

    conversation_history += f"user: {user_message}\nassistant:"

    payload = {
        "inputs": conversation_history,
        "parameters": {
            "max_new_tokens": 128,
            "top_p": 0.9,
            "temperature": 0.7,
            "stop": ["user:", "User:", "\nuser:", "\nUser:"]
        }
    }

    response = predictor.predict(payload)

# extracting response
    if isinstance(response, list) and "generated_text" in response[0]:
        full_output = response[0]["generated_text"]
    elif isinstance(response, dict) and "generated_text" in response:
        full_output = response["generated_text"]
    else:
        full_output = str(response)

# removing that end user string
    assistant_reply = full_output.replace(conversation_history, "").strip()
    if assistant_reply.endswith("user:") or assistant_reply.endswith("User:"):
        assistant_reply = assistant_reply.rsplit("user:", 1)[0].strip()

    print(f"Assistant: {assistant_reply}\n")

    conversation_history += f" {assistant_reply}\n"
