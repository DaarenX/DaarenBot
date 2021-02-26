from src.commands import client
import json

if __name__ == "__main__":
    token = json.load(open("src/config.json"))['token']
    client.run(token)
