import sys
import subprocess
import importlib

print(f"Configuring environment: {sys.executable}")

def install(packages, description):
    print(f"\n--- {description} ---")
    # --no-cache-dir ensures we don't use broken cached downloads
    cmd = [sys.executable, "-m", "pip", "install", "--no-cache-dir"] + packages
    try:
        subprocess.check_call(cmd)
        print("✅ OK")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install {packages}. Error: {e}")

# 1. Upgrade build tools first (Critical for building pandas_ta)
install(["--upgrade", "--force-reinstall", "pip", "setuptools", "wheel"], "Upgrading build tools")

# 2. Remove conflicts
print("\n--- Removing potential conflicts ---")
subprocess.call([sys.executable, "-m", "pip", "uninstall", "-y", "websocket", "pandas-ta", "pandas_ta"])

# 3. Install Numpy 1.x (Critical: pandas_ta breaks with Numpy 2.0)
install(["numpy<2.0.0"], "Installing Numpy 1.x")

# 4. Install Pandas & Scipy (Prerequisites)
install(["pandas<2.0.0", "scipy", "typing_extensions"], "Installing Pandas 1.x & Scipy")

# 5. Install pandas_ta (Now that prereqs are ready)
install(["pandas_ta", "--no-deps"], "Installing pandas_ta")

# 6. Install remaining libraries
install(["streamlit", "plotly", "websocket-client", "requests", "wikipedia", "certifi"], "Installing App Dependencies")

# 7. Verify
print("\n--- Verifying Imports ---")
import_names = {
    "pandas_ta": "pandas_ta",
    "websocket-client": "websocket",
    "streamlit": "streamlit",
    "plotly": "plotly",
    "pandas": "pandas",
    "numpy": "numpy"
}

for package, module in import_names.items():
    try:
        importlib.import_module(module)
        print(f"✅ {module} imported.")
    except ImportError:
        print(f"❌ {module} FAILED to import.")
