import httpx

payload = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "SendMessage",
    "params": {
        "message": {
            "role": "ROLE_USER",
            "messageId": "m-1",
            "parts": [{"text": "AI is changing news. Editors use it daily. Readers notice speed. Costs are falling."}],
        }
    },
}
r = httpx.post(
    "http://127.0.0.1:8002/",
    json=payload,
    headers={"A2A-Version": "1.0"},
)
print(r.json())