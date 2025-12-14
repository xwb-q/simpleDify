import os
from app.core.config import settings

print("=== Configuration Test ===")
print(f"PROJECT_NAME: {settings.PROJECT_NAME}")
print(f"API_V1_STR: {settings.API_V1_STR}")
print(f"DATABASE_URL: {settings.DATABASE_URL}")

# Test Qwen configuration
print("\n=== Qwen Configuration ===")
print(f"QWEN_API_KEY from settings: '{settings.QWEN_API_KEY}'")
print(f"QWEN_API_KEY from env: '{os.getenv('QWEN_API_KEY', '')}'")
print(f"QWEN_BASE_URL from settings: '{settings.QWEN_BASE_URL}'")

# Check all environment variables that might be relevant
print("\n=== Relevant Environment Variables ===")
qwen_vars = {k: v for k, v in os.environ.items() if 'QWEN' in k.upper()}
if qwen_vars:
    for key, value in qwen_vars.items():
        # Mask the API key for security
        masked_value = value[:4] + '*' * (len(value) - 8) + value[-4:] if len(value) > 8 else '*' * len(value)
        print(f"{key}: {masked_value}")
else:
    print("No QWEN environment variables found")

# Check if .env file exists
import os.path
env_path = os.path.join(os.path.dirname(__file__), '.env')
print(f"\n=== Environment File Check ===")
print(f".env file exists: {os.path.exists(env_path)}")
if os.path.exists(env_path):
    print(".env file contents:")
    with open(env_path, 'r') as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                key = line.split('=')[0]
                print(f"  {key}=****")
else:
    print("Consider creating a .env file with your QWEN_API_KEY")

# Test DashScope
print("\n=== DashScope Test ===")
try:
    import dashscope
    print("DashScope SDK imported successfully")
    print("Available attributes:", [attr for attr in dir(dashscope) if not attr.startswith('_')])
except ImportError as e:
    print(f"Failed to import DashScope SDK: {e}")