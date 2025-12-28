import sys
import subprocess
import importlib

packages = [
    "certifi", # Fix SSL issues on Mac
    "streamlit",
    "plotly",
    "pandas",
    "pandas_ta",
    "websocket-client",  # This is the correct library, NOT 'websocket'
    "requests",
    "wikipedia"
]

# Map package names to import names for verification
import_names = {
    "websocket-client": "websocket",
    "pandas_ta": "pandas_ta",
    "streamlit": "streamlit",
    "plotly": "plotly",
    "pandas": "pandas",
    "requests": "requests",
    "wikipedia": "wikipedia"
}

print(f"Installing libraries to environment: {sys.executable}")

# 0. Upgrade pip
print("Upgrading pip...")
subprocess.call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])

# 1. Uninstall conflicting 'websocket' package if it exists (common issue)
print("Checking for conflicting packages...")
subprocess.call([sys.executable, "-m", "pip", "uninstall", "-y", "websocket"])

# 2. Install required packages
for package in packages:
    print(f"Installing {package}...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    except subprocess.CalledProcessError:
        print(f"FAILED to install {package}")

# 3. Verify imports
print("\n--- Verifying Imports ---")
all_good = True
for package, module_name in import_names.items():
    try:
        importlib.import_module(module_name)
        print(f"✅ {module_name} (from {package}) imported successfully.")
    except ImportError as e:
        print(f"❌ {module_name} FAILED to import. Error: {e}")
        all_good = False

if all_good:
    print("\nSUCCESS: All dependencies installed and verified.")
else:
    print("\nWARNING: Some modules failed to load. Check the errors above.")
