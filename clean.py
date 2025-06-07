import json
import jsonlines

def convert_to_chat_format(input_path, output_path):
    with open(input_path, 'r') as infile:
        raw_data = json.load(infile)

    with jsonlines.open(output_path, 'w') as writer:
        progress = 0
        for entry in raw_data:
            print("Done with ",progress) #entry prog print
            dialog = []

            # sys prompt
            topic = entry.get("background_info", {}).get("topic", "unknown topic")
            dialog.append({
                "role": "system",
                "content": f"You are a teacher discussing the topic: {topic}. Be engaging and helpful."
            })
            sub_progress = 0
            last_role = "system"
            for message in entry["conversation"]:
                print(f"Done with {progress}.{sub_progress}") #Printing progress
                # Map roles
                role = message["role"]
                if role == "Teacher":
                    new_role = "assistant"
                elif role == "Student":
                    new_role = "user"
                else:
                    continue  
                
                if role == last_role:
                    continue
                
                content = message["text"].strip().replace('\"\",', '').replace('\",', '').replace('"', '') #removing this random stuff
                dialog.append({
                    "content":content,
                    "role": new_role
                })
                last_role = role
                sub_progress += 1

            writer.write({"dialog": dialog})
            progress += 1

#iterate and cleanup
for number in range(1,6):
    convert_to_chat_format(f"Source/conversations_train{number}.json", f"Cleaned/cleaned_conversations_train{number}.jsonl")
    
