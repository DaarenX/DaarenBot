from src.commands import client, config
import json

if __name__ == "__main__":
    token = config['token']
    client.run(token)
