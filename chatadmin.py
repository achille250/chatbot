import openai
import gradio
import boto3

# Configure AWS credentials
aws_access_key_id = "AKIAW4FKREA7L6Z6VKFY"
aws_secret_access_key = "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"
aws_region = "us-east-1"

# Create a DynamoDB client
dynamodb = boto3.client('dynamodb', region_name=aws_region, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

# OpenAI API key
openai.api_key = "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"

# Create a timestamp for the chat log file
# Calculate MD5 hash of the timestamp
#timestamp = time.strftime("%Y_%m_%d-%H_%M_%S", time.localtime())
#timestamp_hash = hashlib.md5(timestamp.encode()).hexdigest()
# Define a dictionary to store saved responses
saved_responses = {
    "What is Azubi Program?": "Azubi Africa is a tech training program with a proven track record across Africa,we provide tailored trainings to make talents ready for a job in tech (education partner of Microsoft & AWS) >1,000 trainees certified in Ghana, Kenya & Rwanda in 2021 on Microsoft & Amazon Web Services.",
    "how long till I receive feedback, After my application?": "Ideally 2 weeks. If you do not get a response from us after two weeks, please consider your application unsuccessful.",
    "Are there prerequisites or language requirements?": "English language is fundamental.",
    "Are the opportunities open to only Africans?": "No, we thrive in our diversity.",
    "Do you work with PWDs?": "Yes, we have an entire domain dedicated to ensuring their inclusion.",
    "When should I apply?": "Applications are open. Visit https://www.azubiafrica.org/ Click on Apply Now to begin your Application.",
    "program_duration": "Our program typically lasts for 9 months.",
    "tips": "Here are some tips for success in our program...",
    "what is an income share agreement": "Learn, earn, and pay later under our ISA model.",
    "collaboration": "We collaborate with industry leaders and organizations to enhance your learning experience.",
    "what is the enrollment fee": "all learners are required to pay a one-time, non-refundable commitment fee of 100 EUR within the 4-week trial period",
    "what is azubi program":""
}

messages = [{"role": "system", "content": "You are a cloud engineer expert that specializes in AWS infrastrure and Architecture"}]
# Function to save_predefined_responses 
def save_response(user_input, assistant_reply):
    if not assistant_reply.strip():  # Check if assistant_reply is empty or contains only whitespace
        return
    conversation = f"User: {user_input}\nAssistant: {assistant_reply}"
    table_name = "chatbot"  # DynamoDB table name
# Save the conversation to DynamoDB
    response = dynamodb.put_item(
        TableName=table_name,
        Item={
            'user_input': {'S': user_input},
            'assistant_reply': {'S': assistant_reply},
            #'conversation_id': {'S': timestamp_hash},  # Use timestamp as a unique ID
            'conversation': {'S': conversation}
        }
    )
# Save predefined responses
for user_input, assistant_reply in saved_responses.items():
    save_response(user_input, assistant_reply)

def CustomChatGPT(user_input):
    if user_input.lower() == "admin":
        # Admin login
        admin_password = "Admin@123"
        if input("Enter admin password: ") == admin_password:
            admin_response = input("You are logged in as an admin. Enter a new response: ")
            question_area = input("Enter the question (e.g., program_duration): ")
            saved_responses[question_area] = admin_response

            # Save the new question and response to the database
            save_response(question_area, admin_response)
            
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
        # Save the conversation to DynamoDB
        save_response(user_input, ChatGPT_reply)
        return ChatGPT_reply

demo = gradio.Interface(fn=CustomChatGPT, inputs="text", outputs="text", title="Cloud Engineer Expert")

demo.launch(share=True)
