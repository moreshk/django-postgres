from dotenv import load_dotenv
import os
load_dotenv()
print(os.environ.get('EMAIL_PORT'))  # This should print the port number