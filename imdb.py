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
  name="Data visualizer",
  description="You are great at creating beautiful data visualizations. You analyze data present in .csv files, understand trends, and come up with data visualizations relevant to those trends. You also share a brief text summary of the trends observed.",
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
      "content": "Create 3 data visualizations based on the trends in this file.",
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
  content='Create 3 data visualizations based on the data.'
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