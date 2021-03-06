from src.commands import client, config

if __name__ == "__main__":
    token = config['token']
    client.run(token)
