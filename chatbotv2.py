import openai
import gradio
import time
import os

openai.api_key = "YOUR_OPENAI_API_KEY"

timestamp = time.strftime("%Y_%m_%d-%H_%M_%S", time.gmtime())
filename = timestamp + ".txt"

# Define a dictionary to store saved responses
saved_responses = {
    "program_duration": "Our program typically lasts for X months.",
    "tips": "Here are some tips for success in our program...",
    # Add more predefined responses for other question areas
}

messages = [{"role": "system", "content": "You are a financial expert that specializes in real estate investment and negotiation"}]

def save_response(user_input, assistant_reply):
    with open(filename, 'a') as f:
        f.write(f"User: {user_input}\n")
        f.write(f"Assistant: {assistant_reply}\n")

def CustomChatGPT(user_input):
    if user_input.lower() == "admin":
        # Admin login: You can define your own password or authentication mechanism
        admin_password = "your_password_here"
        entered_password = input("Enter admin password: ")
        if entered_password == admin_password:
            admin_response = input("You are logged in as an admin. Enter a new response: ")
            question_area = input("Enter the question area (e.g., program_duration): ")
            saved_responses[question_area] = admin_response
            return f"Response for {question_area} updated."
        else:
            return "Admin login failed. You are not an admin."
    elif user_input in saved_responses:
        return saved_responses[user_input]
    else:
        messages.append({"role": "user", "content": user_input})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        ChatGPT_reply = response["choices"][0]["message"]["content"]
        messages.append({"role": "assistant", "content": ChatGPT_reply})

        # Save the conversation to the text file
        save_response(user_input, ChatGPT_reply)
        return ChatGPT_reply

demo = gradio.Interface(fn=CustomChatGPT, inputs="text", outputs="text", title="Real Estate Pro")

demo.launch(share=True)
