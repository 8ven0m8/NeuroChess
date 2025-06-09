import subprocess

# Path to your python interpreter in .venv
python_path = r"c:/Users/DELL/OneDrive/Desktop/Computer Programming/.venv/Scripts/python.exe"

# Full paths to your scripts
script1 = r"c:/Users/DELL/OneDrive/Desktop/Computer Programming/learning pygame/NeuroChess/app.py"
script2 = r"c:/Users/DELL/OneDrive/Desktop/Computer Programming/learning pygame/NeuroChess/NeuroChess.py"  # replace with your other script

# Run both scripts concurrently, no waiting
p1 = subprocess.Popen([python_path, script1])
p2 = subprocess.Popen([python_path, script2])

print("Both scripts are running...")
p1.wait()
p2.wait()
