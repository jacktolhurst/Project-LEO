import urequests
from dotenv import load_dotenv
import os

load_dotenv() 

data = {
    "content": "test",
}


response = urequests.post(os.getenv('DISCORD_WEBHOOK'), data=data)