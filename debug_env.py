import os
import sys

print("=== Environment Variable Debug Script ===")

# Check if QWEN_API_KEY is in the environment
qwen_api_key = os.environ.get("QWEN_API_KEY", "NOT_FOUND")
print(f"QWEN_API_KEY in os.environ: {qwen_api_key}")

# Check all environment variables that might be related
print("\n=== All Environment Variables ===")
for key, value in sorted(os.environ.items()):
    if "QWEN" in key.upper():
        # Show first 5 chars and mask the rest for security
        masked_value = value[:5] + "*" * (len(value) - 5) if len(value) > 5 else "*" * len(value)
        print(f"{key} = {masked_value}")

# Check if we're running in a virtual environment
print(f"\n=== Runtime Information ===")
print(f"Python executable: {sys.executable}")
print(f"Current working directory: {os.getcwd()}")

# Check if we can import the settings
try:
    from app.core.config import settings
    print(f"Settings.QWEN_API_KEY: {settings.QWEN_API_KEY[:5] + '*' * (len(settings.QWEN_API_KEY) - 5) if len(settings.QWEN_API_KEY) > 5 else '*' * len(settings.QWEN_API_KEY)}")
except Exception as e:
    print(f"Error importing settings: {e}")

# Check parent process info on Windows
if os.name == 'nt':
    try:
        import psutil
        current_process = psutil.Process()
        parent = current_process.parent()
        print(f"Parent process: {parent.name()} (PID: {parent.pid})")
    except ImportError:
        print("psutil not installed, cannot check parent process")
    except Exception as e:
        print(f"Error checking parent process: {e}")