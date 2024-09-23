---
layout: post
title: "Introduction to Concurrency in Python"
date: 2024-09-23
categories: [Reading Python]
---

Concurrency in Python refers to the ability of a program to perform multiple tasks simultaneously, or at least make it *appear* that multiple tasks are being executed simultaneously. Python offers several models of concurrency: 

1. **Thread-based concurrency**(using the `threading` module)
2. **Process-based concurrency** (Using the  `multiprocessing` module)
3. **Asynchronous I/O**(Using the  `asyncio` module) 
4. **Concurrent futures**(using the  `concurrent.futures` module). 

## 1. Thread-based Concurrency

- Threads allow parallel execution of tasks. A thread is lightweight unit of process execution, but Python's Global Interpreter Lock(GIL) ensures that only one thread runs at a time per python process, limiting true parallelism for CPU-bound tasks 

**Best suited for**: 
  - I/O-bound tasks like reading from disk, web-scraping, network I/O etc 

**example** 


```python
import threading 
import time 

def worker(): 
    print(f"worker thread started")
    time.sleep(2)
    print(f"worker thread finished")

#Create two threads 
thread1 = threading.Thread(target=worker)
thread2 = threading.Thread(target=worker)

#start threads 
thread1.start() 
thread2.start() 

#Waiting for both threads to complete 
thread1.join()
thread2.join() 

print("Both threads completed")
```

    worker thread started
    worker thread started
    worker thread finished
    worker thread finished
    Both threads completed


**Key Points**: 
1. Threads share the same memory space
2. Python's GIL limits true parallel execution for CPU-bound tasks
3. Great for I/O bound tasks like network requests, file I/0 etc

## 2. Process-based concurrency( `multiprocessing` module )

  `multiprocessing`  module creates separate processes. Each process has its own python interpreter and memory space, bypassing the GIL. This makes  `multiprocessing` suitable for CPU-bound tasks, as each process runs on a different CPU core. 
  - **Best suited for?** 
        - CPU-bound tasks(e.g heavy computation, matrix operations)
  


```python
import multiprocessing 
import time

def worker(): 
    print(f"Worker process started")
    time.sleep(2)
    print(f"Worker process finished")

#Creates two processes 
process1 = multiprocessing.Process(target=worker)
process2 = multiprocessing.Process(target=worker)

#Start process 
process1.start() 
process2.start() 

#wait for both processes to complete 
process1.join() 
process2.join() 

print("Both Processes completed")
```

    Both Processes completed


**Key Points**
- Each process has its own memory space, eliminating the GIL problem 
- Processes don't share memory easily, requiring inter-process communication (IPC) like queues, pipes, or shared memory
- Higher overhead compared to threads due to process creation 

## 3. Asynchronous programming( `asyncio` module)
-  `asyncio` is designed for single-threaded, single-process concurrency , where tasks are run asynchronously. Instead of blocking for I/O operations, tasks await the result while other tasks are allowed to run. It's highly efficient for I/O-bound programs but doesn't involve true parallelism like threads or processes. 
-   **best suited for**
    -   High-concurrency, I/O-bound tasks(e.g network requests, file I/O)   


```python
import asyncio

async def worker():
    print("Worker started")
    await asyncio.sleep(2)  # Simulates I/O-bound operation
    print("Worker finished")

async def main():
    task1 = asyncio.create_task(worker())
    task2 = asyncio.create_task(worker())

    await task1
    await task2

# If you're in an environment with an already running event loop, use `await` instead of `asyncio.run()`
await main()

```

    Worker started
    Worker started


    Worker finished
    Worker finished


## 4. Concurrent Futures( `concurrent.futures` Module )
 - `concurrent.futures` is a high-level interface for both threads and processes. 
 -  It abstracts threading and multiprocessing with the  `ThreadPoolExecutor`  and  `ProcessPoolExecutor`  classes.You submit tasks, which return  `Future` objects that represent the results of async operations 
  
  **Best suited for**: 
   - Both I/O-bound and CPU-bound tasks, depending on whether threads or processes are used. 


```python
from concurrent.futures import ThreadPoolExecutor
import time 

def worker():
    print("Worker started")
    time.sleep(2)
    print("worker finished")

with ThreadPoolExecutor(max_workers=2) as executor: 
    future1 = executor.submit(worker)
    future2 = executor.submit(worker)

#Block until results are available 
print(future1.result())
print(future2.result())
```

    Worker startedWorker started
    
    worker finishedworker finished
    
    None
    None


**Key Points**
- The same  interface can handle both threads(`ThreadPoolExecutor`)and processes(`ProcessPoolExecutor`)
- Makes it easy to submit jobs and retrieve their results via  `Future` objects 

## Concurrency and GIL
- Python's GIL(Global Interpreter Lock) afects CPU-bound programs running in threads, as only one thread can execute Python bytecode at a time. For CPU-bound tasks, use the  `multiprocessing` module, which runs processes instead of threads and avoids the GIL

### Why does the Python's Global interpreter Lock limit parallelism?
- This is a mechanism in CPython that ensures that only one thread executes Python bytecode at a time, even if the program has multiple threads. This design choice simplifies memory management
- Here's a breakdown of why Python uses the GIL and the trade-offs involved
- 
#### **Memory Management and Reference counting**

        1. One of the primary reasons for the GIL is CPython memory management, specifically its use of **reference counting** for garbage collection. In Python, each object has an associated reference count that tracks how many references to that object exist

#### Example
   
  ```Python
  a = []
  b = a # Reference count of the list increases by 1
  ```
- When the reference count of an object drops to zero, the memory associated with that object is freed
  - Without the GIL, multiple threads accessing and modifying the reference counts simultaneously could lead to **race conditions**. Two threads could try to modify the reference count of the same object at the same time, corrupting the memory management system. 
  - The GIL ensures *thread safety* by allowing only one thread to execute Python bytecode at a time. This eliminates the need for locking mechanism around reference counting

#### **Simplifying C extensions** 
Python's GIL simplifies the writing of C extensions for Python. Many external libraries, especially those written in C, expect to handle data structures without worrying about concurrency. The GIL ensures that they don't need to implement thread-safety mechanisms in their code

#### **Historical reason**
When Python ws first designed in the late 1980s and early 1990s, **threading** and **multi-core** processors were not as common or as important as they are today. The GIL was a simple and effective way to handle concurrency for I/O-bound tasks, which was the primary use case at the time. Removing the GIL later, when Python was more widely used, became complicated due to backward compatibility concerns and the need to maintain efficiency 

 #### **Trade-Offs: GIL's impact on Performance**
   - *pros*
   - **simplicity**: The GIL's makes the implementation of Cpython simpler. It avoids complex locking mechanisms that would need to be added to memory management, which would slow down single-threaded code execution
   - **single-threaded performane**: The GIL allows Python to avoid frequent locking and unlocking in single-threaded programs, meaning that single-threaded apps run efficiently

  - *cons*
  - **CPU-bound tasks in multithreaded programs** The GIL severely limits multi-threaded performance for CPU-bound tasks (like computations). Even if you create multiple threads, only one thread can execute Python bytecode at any given time. So, multi-core systems can't fully utilize their CPUs for parallel processing in CPU-bound Python code 
  -  **I/O-bound tasks**: For I/O-bound tasks, the GIL doesn't pose much of an issue because threads spend a lot of time waiting for I/O operations (like reading from a disk or a network). During these waits, the GIL is released, allowing other threads to run. 
  
#### **Is it Possible to Remove the GIL?** 
There have been several attempts to remove the GIL, such as: 
- **PyPy**: An alternative implementation of Python, which aims to remove the GIL while optimising performance. However, PyPy has not been fully successful in eliminating the GIL without performance penalties
- **Larry Hastings Gilectomy**: A project aimed at removing the GIL in CPython. While it succeeded in eliminating the GIL, it showed significant performance degradation in single-threaded applications due to the overhead of fine-grained locking mechanisms



