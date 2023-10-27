import openai #module for chatgpt
import gradio #module for user interface
import time
import os

openai.api_key = "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"

timestamp = time.strftime("%Y_%m_%d-%H_%M_%S", time.gmtime())
filename = timestamp + ".txt"


    #with open(filename, 'w') as f:
        #f.write("User: Welcome to OpenAI chat!\n")

messages = [{"role": "system", "content": "You are a financial experts that specializes in real estate investment and negotiation"}]

def CustomChatGPT(user_input):
    messages.append({"role": "user", "content": user_input})
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = messages
    )
    ChatGPT_reply = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": ChatGPT_reply})

    # Save the reply to the text file
    if not os.path.exists(filename):
       with open(filename, 'a') as f:
        f.write(f"User: {user_input}\n")
        f.write(f"Assistant: {ChatGPT_reply}\n")
    return ChatGPT_reply

demo = gradio.Interface(fn=CustomChatGPT, inputs = "text", outputs = "text", title = "Real Estate Pro")

demo.launch(share=True)