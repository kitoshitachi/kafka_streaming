import os, time

os.system("start cmd /k python topic.py create")
time.sleep(5)
# os.system(f"start cmd /k python worker-0.py")
# os.system(f"start cmd /k python worker-0.py")
# os.system(f"start cmd /k python worker-0.py")
os.system(f"start cmd /k python worker-1.py")
os.system(f"start cmd /k python worker-1.py")
os.system(f"start cmd /k python worker-1.py")
os.system("start cmd /k python user.py test.csv")

