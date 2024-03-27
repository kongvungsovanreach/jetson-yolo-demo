import threading
import time

# Define a function for the first thread
def thread_function1():
    for i in range(5):
        print("Thread 1 is running")
        time.sleep(1)

# Define a function for the second thread
def thread_function2():
    for i in range(5):
        print("Thread 2 is running")
        time.sleep(1)

# Create threads
thread1 = threading.Thread(target=thread_function1)
thread2 = threading.Thread(target=thread_function2)

# Start threads
thread1.start()
thread2.start()

# Wait for both threads to complete
thread1.join()
thread2.join()

print("Both threads have finished")
