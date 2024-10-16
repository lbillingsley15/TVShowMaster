from dotenv import load_dotenv

load_dotenv()
from openai import OpenAI
client = OpenAI()
import os
#capability to read files
file = client.files.create(
    file = open('IMDB_top_1000.csv', 'rb'),
    purpose = 'assistants'
)
assistant = client.beta.assistants.create(
  name="python coder",
  description="You are the world's best python code generator. You specialized in using the matplotlip for data visualization. You answer with actual python code that can be run outside of the thread.",
  model="gpt-4o",
  tools=[{"type": "code_interpreter"}],
  tool_resources={
    "code_interpreter": {
      "file_ids": [file.id]
    }
  }
)
thread = client.beta.threads.create(
  messages=[
    {
      "role": "user",
      "content": "Based on the trends in this file, provide python code for creating 3 unique visualizations.",
      "attachments": [
        {
          "file_id": file.id,
          "tools": [{"type": "code_interpreter"}]
        }
      ]
    }
  ]
)
#create a message
message = client.beta.threads.messages.create(
  thread_id=thread.id,
  role='user',
  content='Generate python code to create 3 unique data visualizations.'
)

#create a run
run=client.beta.threads.runs.create_and_poll(
  thread_id=thread.id,
  assistant_id=assistant.id,
  instructions="Please address the user as Prince Charming."
)
#output
if run.status == 'completed':
  messages = client.beta.threads.messages.list(
    thread_id=thread.id
  )
  print(messages)
  with open('dataviz.txt', "w") as f:
    print(messages, file = f)