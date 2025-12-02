import os
import subprocess

# Check if virtual environment is active
if not os.getenv('VIRTUAL_ENV'):
    print("Warning: It is recommended to run inside a virtual environment.")

# Install dependencies if requirements.txt exists
if os.path.exists("requirements.txt"):
    print("Installing dependencies...")
    subprocess.check_call(["pip", "install", "-r", "requirements.txt"])

print("Starting Flask app...")
os.environ["FLASK_APP"] = "app.py"
os.environ["FLASK_ENV"] = "development"
os.environ["FLASK_DEBUG"] = "1"

subprocess.run(["flask", "run"])
