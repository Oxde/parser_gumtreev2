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
        'vip': [], - chat_id to send ads
        'active_chat_ids': [],
        'chats_ids_dict': {: 0,: 0,: 0} #should be number of chat before :
    }
    asyncio.run(save_configuration('config.json', ultimative_memory))
