import os, json, openai, requests

# -------------------------------------------------
# 1)  Set your OpenAI API key in the environment
#     PowerShell (once per terminal):
#       $Env:OPENAI_API_KEY="sk..."
# -------------------------------------------------
openai.api_key = os.getenv("OPENAI_API_KEY")        # <-- keep None if not set
if openai.api_key is None:
    raise RuntimeError("Set $Env:OPENAI_API_KEY first!")

FUNCTION_URL = "https://us-central1-pc-operator-prod.cloudfunctions.net/enqueueCommand"
FUNCTION_KEY = "xSuperSecretLongTokenx"

functions = [
    {
        "name": "enqueueCommand",
        "description": "Run a shell or AHK command on the PC",
        "parameters": {
            "type": "object",
            "properties": {
                "action":  { "type": "string", "enum": ["shell", "ahk"] },
                "payload": {
                    "type": "object",
                    "properties": {
                        "cmd":    { "type": "string" },
                        "script": { "type": "string" }
                    },
                    "description": "For shell use {cmd}, for AHK use {script}"
                }
            },
            "required": ["action", "payload"]
        }
    }
]

# -------------------------------------------------
def main():
    user_prompt = (
        "Please use AutoHotkey v2 syntax. "
        + input("What command do you want to run? ")
    )

    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": user_prompt}],
        functions=functions,
        function_call="auto"
    )

    msg = resp.choices[0].message
    if msg.get("function_call"):
        args = json.loads(msg.function_call.arguments)
        print(">>> Enqueuing:", args)
        r = requests.post(
            FUNCTION_URL,
            headers={
                "Content-Type": "application/json",
                "x-api-key": FUNCTION_KEY
            },
            json=args
        )
        print("Cloud Function returned:", r.json())
    else:
        print("Model didn’t call the function. Response:", msg.content)

# -------------------------------------------------
if __name__ == "__main__":
    main()
