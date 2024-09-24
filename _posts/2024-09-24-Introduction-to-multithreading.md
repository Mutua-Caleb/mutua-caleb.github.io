---
layout: post
title: "Introduction to Multithreading in Python"
date: 2024-09-24
categories: [Reading Python]
---

- A thread is the smallest unit of execution in a program. Multiple threads can run concurrently(not in parallel, due to Python's GIL)
- Threads share the same memory space, making them efficient for tasks that require access to shared data. However, this also leads to challenges, such as **race conditions**
- The  `threading` module provides tools to manage and synchronize threads

#### How Do we Create Threads? 
- The simplest way to create a thread is to use the  `Thread`  class from the  `threading` module. You can either pass a function to  `Thread`, or subclass it and override the  `run`  



```python
import threading
import time 

#  simple function to run in a thread
def worker(): 
    print("Worker thread started")
    time.sleep(2)
    print("Worker thread finished")

#Creating threads
thread1 = threading.Thread(target=worker)
thread2 = threading.Thread(target=worker)

# Starting threads
thread1.start()
thread2.start()

#Waiting for threads to finish 
thread1.join()
thread2.join()

print("Both threads completed")
```

    Worker thread started
    Worker thread started
    Worker thread finished
    Worker thread finished
    Both threads completed


- `threading.Thread(target=worker)` : creates a thread that will execute the  `worker`  function 
-  `start()` : starts the thread's activity
-   `join`: waits for the thread to complete before the main thread continues  

**Example 2: subclassing  `Thread`** 


```python
import threading
import time

class WorkerThread(threading.Thread):
    def run(self):
        print(f"Worker thread {self.name} started")
        time.sleep(2)
        print(f"Worker thread {self.name} finished")

#Creating threads
thread1 = WorkerThread() 
thread2 = WorkerThread() 

#starting threads 
thread1.start()
thread2.start() 

#Waiting for threads to finish 
thread1.join()
thread2.join() 

print("Both threads completed")
```

    Worker thread Thread-11 started
    Worker thread Thread-12 started
    Worker thread Thread-12 finishedWorker thread Thread-11 finished
    
    Both threads completed


- Here, create a custom thread class by subclassing  `Thread`  and overriding the  `run`  method, which contains the code that runs when the thread is started. 

#### **Thread Synchronization**
- When multiple threads access shared resources (like data or files), it's important to **synchronize** access to avoid race conditions, where multiple threads modify a shared resource concurrently, leading to inconsistent results

##### Locking Mechanism 
- The  `threading` module provides a **Lock** or **Mutex** to ensure that only one thread accesses a critical section of code at a time


```python
import threading

balance = 0 #shared resource
lock = threading.Lock() 

def deposit(amount): 
    global balance
    with lock: #Only one thread can modify the balance at a time 
        current_balance = balance 
        current_balance +=amount
        balance = current_balance

threads = []
for i in range(10): #create 10 threads 
    t = threading.Thread(target=deposit, args=(100,))
    threads.append(t)
    t.start() 

# Wait for all threads to finish
for t in threads: 
    t.join() 
print(f"Final balance: {balance}")


```

    Final balance: 1000


Here: 
-  `lock = threading.Lock()`: A lock object is created
-   `with lock`: Ensures only one thread at a variable executes the code block that modifies the shared  `balance` variable. This prevents race conditions 
-   Without the lock, different, different threads might access  `balance` simultaneously, leading to incorrect results. 

#### **Thread communication** 
When you have multiple threads running, sometimes they need to communicate with each other. Python provides  `Queues`  for safe thread communication 

**Using queue.Queue**



```python
import threading
import queue
import time 

#Create a shared queue 
task_queue = queue.Queue()

def worker(): 
    while True: 
        task = task_queue.get() # Get a task from the queue 
        if task is None: #Stop if we receive None 
            break 
        print(f"Processing task: {task}")
        time.sleep(1)
        task_queue.task_done() #Signal that the task is done 

#Creating and starting worker threads 
threads = []
for _ in range(3): 
    t = threading.Thread(target = worker)
    threads.append(t)
    t.start() 

#Adding tasks to the queue 
for i in range(5): 
    task_queue.put(f"Task-{i}")

#wait for all tasks to be processed 
task_queue.join() 

#Stopping the worker threads
for _ in range(3): 
    task_queue.put(None)

# Wait for all threads to complete 
for t in threads: 
    t.join() 

print("All tasks completed")
```

    Processing task: Task-0Processing task: Task-1
    
    Processing task: Task-2
    Processing task: Task-3Processing task: Task-4
    
    All tasks completed


- `queue.Queue()` : A thread-safe queue used for communication between threads
- `task_queue.get()`: Retrieves a task from the queue. If the queue is empty, it blocks until an item becomes available
- `task_queue.task_done()` : signals that a task is complete 
- `task_queue.put()`: Adds a  task to the queue
- This design pattern(Worker threads consuming tasks from a queue) is common in concurrent programming


#### **Daemon Threads**
- A **daemon thread** is a thread that runs in the background and is terminated automatically when the main program exits, meaning it will not prevent the program from terminating


```python
import threading
import time

def background_worker(): 
    while True: 
        print("Background thread running")
        time.sleep(1)
        

#Create a daemon thread 
t = threading.Thread(target=background_worker, daemon=True)
t.start() 

#Main thread sleeps for 3 seconds before exiting 
time.sleep(3)
print("Main thread exiting")
```

- The above code will run forever because we forgot to tell the background_worker to stop. so even after we've exited the main thread, it will continue to run since we didn't exit it. 
- To fix this, we'll need to tell it explictly to stop. It's like the main thread saying, "when I am done, you should also stop" 
- Here's the fix


```python
import threading 
import time 

stop_flag = threading.Event() 

def background_worker(): 
    while not stop_flag.is_set(): 
        print("Background thread running")
        time.sleep(1)

#Create a daemon thread 
t = threading.Thread(target=background_worker, daemon = True)
t.start() 

#Main thread sleeps for 3 seconds before exiting 
time.sleep(3)
print("main thread exiting")
stop_flag.set() 
t.join() 
```

    Background thread running
    Background thread running
    Background thread running
    main thread exitingBackground thread running
    

