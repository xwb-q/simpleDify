import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

print("Testing environment variable access:")
print("=" * 40)

# Test 1: Check if QWEN_API_KEY is available in environment
qwen_api_key = os.environ.get("QWEN_API_KEY", "")
print(f"QWEN_API_KEY from os.environ.get(): '{qwen_api_key}'")

# Test 2: Check all environment variables containing "QWEN"
print("\nAll QWEN-related environment variables:")
for key, value in os.environ.items():
    if "QWEN" in key.upper():
        # Mask the value for security if it's likely an API key
        masked_value = value[:5] + "*" * (len(value) - 5) if len(value) > 5 and value != "your_actual_qwen_api_key_here" else value
        print(f"{key}: {masked_value}")

# Test 3: Check if dotenv is working by looking for the .env file
import os.path
env_file_path = os.path.join(os.path.dirname(__file__), '.env')
env_example_path = os.path.join(os.path.dirname(__file__), '.env.example')
env_tem_path = os.path.join(os.path.dirname(__file__), '.env.tem')

print(f"\n.env file exists: {os.path.exists(env_file_path)}")
print(f".env.example file exists: {os.path.exists(env_example_path)}")
print(f".env.tem file exists: {os.path.exists(env_tem_path)}")

if os.path.exists(env_file_path):
    print(f"\nContents of .env file:")
    try:
        with open(env_file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key_value = line.strip().split('=', 1)
                    if len(key_value) == 2:
                        key, value = key_value
                        masked_value = value[:3] + "*" * (len(value) - 3) if len(value) > 3 and value != "your_actual_qwen_api_key_here" else value
                        print(f"  {key}={masked_value}")
    except UnicodeDecodeError:
        with open(env_file_path, 'r', encoding='gbk') as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key_value = line.strip().split('=', 1)
                    if len(key_value) == 2:
                        key, value = key_value
                        masked_value = value[:3] + "*" * (len(value) - 3) if len(value) > 3 and value != "your_actual_qwen_api_key_here" else value
                        print(f"  {key}={masked_value}")
    print("\nNote: If the QWEN_API_KEY still appears empty, make sure to:")
    print("  1. Replace 'your_actual_qwen_api_key_here' with your actual API key in the .env file")
    print("  2. Restart your Python environment/IDE to reload the environment variables")
else:
    print("No .env file found.")

# Test 4: Check the settings module directly
try:
    from app.core.config import settings
    print(f"\nValue from settings.QWEN_API_KEY: '{settings.QWEN_API_KEY}'")
except Exception as e:
    print(f"\nError importing settings: {e}")