import os, time
from settings import NUM_PARTITIONS

cmd = 'start cmd /k python'

os.system(f"{cmd} topic.py create")
time.sleep(5)
for _ in range(NUM_PARTITIONS):
    # os.system(f"{cmd} worker-0.py") # run tfidf for low model
    os.system(f"{cmd} worker-1.py") #run w2v for high model
    # os.system(f"{cmd} worker-2.py") # run low model svm
    # os.system(f"{cmd} worker-4.py") # run low model nb

    os.system(f"{cmd} worker-3.py") # run high model cnn


os.system(f"{cmd} user.py test.csv")

