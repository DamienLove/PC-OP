import os, json
import openai
import requests

# 1) Set your OpenAI key in your environment:
#    Windows PowerShell:  $env:OPENAI_API_KEY="sk-…"
openai.api_key = os.getenv("OPENAI_API_KEY")
FUNCTION_URL = "https://us-central1-pc-operator-prod.cloudfunctions.net/enqueueCommand"
FUNCTION_KEY = "xSuperSecretLongTokenx"

functions = [
  {
    "name": "enqueueCommand",
    "description": "Run a shell or AHK command on the PC",
    "parameters": {
      "type": "object",
      "properties": {
        "action": {
          "type": "string",
          "enum": ["shell","ahk"]
        },
        "payload": {
          "type": "object",
          "properties": {
            "cmd":    {"type": "string"},
            "script": {"type": "string"}
          },
          "required": ["cmd"],
          "description": "For shell use {cmd}, for AHK use {script}"
        }
      },
      "required": ["action","payload"]
    }
  }
]


def main():
    user_prompt = input("What command do you want to run? ")
    resp = openai.ChatCompletion.create(
      model="gpt-4o-mini",
      messages=[{"role":"user","content":user_prompt}],
      functions=functions,
      function_call="auto"
    )
    msg = resp.choices[0].message
    if msg.get("function_call"):
        args = json.loads(msg.function_call.arguments)
        print(f">>> Enqueuing: {args}")
        r = requests.post(
          FUNCTION_URL,
          headers={
            "Content-Type":"application/json",
            "x-api-key": FUNCTION_KEY
          },
          json=args
        )
        print("Cloud Function returned:", r.json())
    else:
        print("Model didn’t call the function. Response:", msg.content)

if __name__ == "__main__":
    main()
