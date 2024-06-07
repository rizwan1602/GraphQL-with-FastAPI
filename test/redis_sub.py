import redis
import json
import pprint
import os

# Redis configuration
redis_host = "localhost"
redis_port = 6379
redis_channel = "robots_live_data"

# Flag to clear the screen
clear_screen = True

# Initialize the Redis client
r = redis.Redis(host=redis_host, port=redis_port, db=0)
pubsub = r.pubsub()
pubsub.subscribe(redis_channel)

print(f"Subscribed to {redis_channel} channel. Waiting for messages...\n")

# Pretty printer for formatted output
pp = pprint.PrettyPrinter(indent=4)

# Function to clear the screen
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# Listen for messages
for message in pubsub.listen():
    if message['type'] == 'message':
        data = json.loads(message['data'])
        if clear_screen:
            clear()
        pp.pprint(data)

