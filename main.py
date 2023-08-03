import openai


def read_api_key(file_path):
    with open(file_path,'r') as file:
        text_context = file.read()
    return text_content.strip()
file_path = 'cgpt4 key.txt'
text_content = read_api_key(file_path)
openai.api_key = text_content

def write_to_js(file_path, text_content):
    with open(file_path, 'w') as file:
        file.write(text_content)
js_file_path = 'output.js'
write_to_js(js_file_path, text_content)


read_api_key()
write_to_js()

chat_log= []

while True:
    user_message = input()
    if user_message.lower() == "quit":
        print(chat_log)
        break
    else:
        chat_log.append({"role" : "user", "content": user_message})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=chat_log
        )

        assistant_response = response['choices'][0]['message']['content']
        print("ChatGPT:", assistant_response.strip("\n").strip())
        chat_log.append({"role": "assistant", "content": assistant_response.strip("\n").strip()})
