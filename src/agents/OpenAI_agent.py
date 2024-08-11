# Importing necessary libraries
from uagents import Agent, Context
from uagents.setup import fund_agent_if_low
from uagents import Model
from openai import OpenAI
client = OpenAI(
    api_key = "replace your OPENAI api key here" #replace your OPENAI api key here
)

# Defining a model for messages
class Message(Model):
    message: str

# Defining the user agent
OpenAI_agent = Agent(
    name="OpenAI Agent",
    port=8001,
    seed="OpenAI Agent secret phrase",
    endpoint=["http://localhost:8001/submit"],
)
 
print(OpenAI_agent.address)
# Funding the user agent if its wallet balance is low
fund_agent_if_low(OpenAI_agent.wallet.address())

print("Chat session has started. Type 'quit' to exit.")

# Function to handle incoming messages
async def handle_message(message):
   
    while True:
        # Get user input
        user_message = message
        
        # Check if the user wants to quit the conversation
        if user_message.lower() == 'quit':
            return "Exiting chat session."
            
        # Send the message to the chat session and receive a streamed response
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages = {user_message}
        )
        
        # Initialize an empty string to accumulate the response text
        full_response_text = ""
        
        # Accumulate the chunks of text
        for chunk in response:
            full_response_text += chunk.text
            
        # Print the accumulated response as a single paragraph
        message = "OpenAi: " + full_response_text
        return message
        
# Event handler for agent startup
@OpenAI_agent.on_event('startup')
async def address(ctx: Context):
    # Logging the agent's address
    ctx.logger.info(OpenAI_agent.address)

# Handler for query given by user
@OpenAI_agent.on_message(model=Message)
async def handle_query_response(ctx: Context, sender: str, msg: Message):
    # Handling the incoming message
    message = await handle_message(msg.message)
    
    # Logging the response
    ctx.logger.info(message)
    
    # Sending the response back to the sender
    await ctx.send(sender, Message(message=message))