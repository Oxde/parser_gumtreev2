import json
import asyncio
import time

async def load_configuration(filename):
    try:
        with open(filename, 'r') as f:
            config_data = json.load(f)
        return config_data
    except (FileNotFoundError, json.JSONDecodeError):
        return None

async def save_configuration(file_path, config_dict):
    with open(file_path, 'w') as config_file:
        json.dump(config_dict, config_file, indent=4)


if __name__ == '__main__':
    ultimative_memory = {
        'vip': [371348044, 5613237024, 770310010],
        'active_chat_ids': [],
        'chats_ids_dict': {371348044: 0, 5613237024: 0, 770310010: 0}
    }
    asyncio.run(save_configuration('config.json', ultimative_memory))