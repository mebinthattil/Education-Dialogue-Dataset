import json
import jsonlines

def convert_to_chat_format(input_path, output_path):
    with open(input_path, 'r') as infile:
        raw_data = json.load(infile)

    with jsonlines.open(output_path, 'w') as writer:
        progress = 0
        for entry in raw_data:
            print("Done with ",progress) #PRINTING PROGRESS
            dialog = []

            # Optional: add a system prompt for context
            topic = entry.get("background_info", {}).get("topic", "unknown topic")
            dialog.append({
                "role": "system",
                "content": f"You are a teacher discussing the topic: {topic}. Be engaging and helpful."
            })
            sub_progress = 0
            for message in entry["conversation"]:
                print(f"Done with {progress}.{sub_progress}")
                # Map roles
                role = message["role"]
                if role == "Teacher":
                    new_role = "assistant"
                elif role == "Student":
                    new_role = "user"
                else:
                    continue  # skip unknown roles

                # Clean text and map to expected format
                content = message["text"].strip().replace('\"\",', '').replace('\",', '').replace('"', '')
                dialog.append({
                    "content": content,
                    "role": new_role
                })
                sub_progress += 1

            writer.write({"dialog": dialog})
            progress += 1

# Example usage
convert_to_chat_format("conversations_train4.json", "cleaned_conversations_train4.jsonl")
convert_to_chat_format("conversations_train5.json", "cleaned_conversations_train5.jsonl")
