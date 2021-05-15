import threading
from objectDetection import startObjectDetection
from assistant import runAssistant

if __name__ == "__main__":
  t1 = threading.Thread(target = runAssistant)
  t2 = threading.Thread(target = startObjectDetection)
  t1.start()
  t2.start()
  t1.join()
  t2.join()