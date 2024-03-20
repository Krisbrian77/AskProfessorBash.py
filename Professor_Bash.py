import os                                             import json                                           import requests                                       import subprocess                                     from datetime import datetime
import time
                                                      def save_to_file(question, answer):                       with open("Capt_logs.txt", "a") as file:                  file.write(f"{datetime.now().strftime('%Y-%m-%d %I:%M %p')}: Question: {question}\n")
        file.write(f"{datetime.now().strftime('%Y-%m-%d %I:%M %p')}: Answer: {answer}\n\n")                                                                       def extract_bash_code(response):                          bash_code = []                                        for choice in response['choices']:                        message = choice['message']['content']                code_blocks = extract_code_from_message(message)
        bash_code.extend(code_blocks)                     return bash_code                                                                                        def extract_code_from_message(message):                   code_blocks = []                                      start_index = message.find("```bash")                 while start_index != -1:
        end_index = message.find("```", start_index + 7)
        if end_index != -1:
            code_blocks.append(message[start_index:end_index + 3])
        start_index = message.find("```bash", end_index + 3)
    return code_blocks

def save_bash_code_to_file(bash_code, file_name=None):
    if not file_name:
        file_name = input("Type in the filename to name this file yourself or press Enter to automatically generate file name: ")
        if not file_name:
            file_name = f"bash_script_{datetime.now().strftime('%Y%m%d%H%M%S')}.sh"
    with open(file_name, "w") as file:
        file.write("#!/bin/bash\n")  # Add shebang line
        for code_block in bash_code:
            # Remove leading and trailing whitespace
            code_block = code_block.strip()
            # Remove leading ```bash and trailing ```
            code_block = code_block.replace("```bash", "").replace("```", "")
            file.write(code_block + "\n\n")
    print_typing(f"\nBash code extracted and saved to {file_name}\n")
    # Change file permissions
    os.chmod(file_name, 0o755)
    return file_name

def execute_bash_script(file_name):
    try:
        subprocess.run(["./" + file_name], check=True)
    except subprocess.CalledProcessError as e:
        print_typing(f"Error: {e}")
        print_typing(f"Failed to execute {file_name}")

def type_out(text):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(0.03)  # Adjust the delay here for typing speed
    print()

def print_typing(text):
    type_out(text)

# Define the alias command
alias_command = "alias Ask='python AskProfessorBask.py'"

# Execute the alias command
os.system(alias_command)

url = "https://chat.tune.app/api/chat/completions"
headers = {
    "Authorization": "tune-faa88cbb-18f8-4a97-a909-b1fae72430c81710549351",
    "Content-Type": "application/json"
}
model = "goliath-120b-16k-gptq"

print_typing("\nProfessor Bash is ready to help. Type 'help' if you're a new user or 'e' to exit chat.")

while True:
    user_input = input("\nAsk Professor Bash >> ")

    if user_input.lower() == 'help':
        print_typing("\nTo chat with Professor Bash and ask him questions you can either type in\n"
              "  'python AskProfessorBash.py', hit enter then type in your question when prompted, example\n"
              "\npython AskProfessorBash.py\n"
              "                 \n"
              "   type 'python AskProfessorBash.py' followed by your question to start the conversation. For example\n"
              "\npython AskProfessorBash.py What is Bash script\n"
              "\nI prefer to use an alias command:\n"
              "\n 'alias ask='python AskProfessorBash.py', \n"
              "then i can just type 'ask' followed by your question then hit enter to start the chat. For example\n"
              "\nask what's Bash script\n")
        continue

    if user_input.lower() == 'e':
        print_typing("\nExiting conversation.")
        break

    elif user_input.strip() != '':
        data = {
            "temperature": 0.5,
            "messages": [
                {
                    "role": "system",
                    "content": "Your name is Professor Bash, if asked what your name is you always answer Professor Bash. You are an expert in coding with bash script and the best in the world at coding in bash script, you know everything about bash script and create the best bash scripts in the world. You always answer any question I ask about Bash Script and write all of the bash script code I ask you to write. You know everything there is to know about bash script. You know every bash script command and how to use every bash script command. You are an excellent teacher and love teaching people how to use bash script. You love writing bash script code and can write any type of bash script anyone needs"
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ],
            "model": model,
            "stream": False,
            "max_tokens": 1000
        }

        response = requests.post(url, headers=headers, json=data)
        response_json = response.json()
        answer = response_json['choices'][0]['message']['content']

        print_typing("\nProfessor Bash Says >>\n")
        print_typing(answer)

        bash_code = extract_bash_code(response_json)
        if bash_code:
            user_choice = input("\nWould you like to:\n1. Save the file\n2. Save the file and run it\n3. Or press Enter not to save the file and not run the code\n>> ")
            if user_choice == '1' or user_choice == '2':
                file_name = save_bash_code_to_file(bash_code)
                if user_choice == '2':
                    execute_bash_script(file_name)
            save_to_file(user_input, answer)
        else:
            print_typing("\nNo bash code found in the response.\n")
            save_to_file(user_input, answer)
