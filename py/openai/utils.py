import os
from dotenv import load_dotenv

load_dotenv() 
# a function check_env_var to check existance of an environment variable
def check_env_var(env_var):
    if env_var in os.environ:
        return True
    else:
        return False

def check_and_exit(env_var):
    if not check_env_var(env_var):
        print(f"{env_var} not found")
        exit(1)

def get_env_var(env_var):
    if check_env_var(env_var):
        return os.environ.get(env_var)
    else:
        return None

def get_api_key():
    return get_env_var("OPENAI_API_KEY")