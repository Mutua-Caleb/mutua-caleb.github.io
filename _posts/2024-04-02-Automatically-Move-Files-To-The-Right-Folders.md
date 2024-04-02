---
layout: post
title: "Automatically Move files to the Right Folders"
date: 2024-04-02
---

My computer is usually messy. When I download files from the internet, they all end up in my Windows Download folder. However, when I later check my Downloads folder, everything looks disorganized and cluttered. Honestly, this affects my ability to think clearly. Surprisingly, maintaining organized digital space is crucial for my mental well-being. 

Enough with the anecdotes. I've devised a solution: whenever I download files such as **epub**, **pdf**, **m4a**, **mp3**, or **weba** from the internet, I want them to be automatically sorted into their respective folders. For example, **epub** and **pdf** files should go to *C:\Users\User\Documents*, **m4a**, **mp3**, and **weba** files to *C:\Users\User\Music*, and **mp4** files to *C:\Users\User\Videos.*

I would like for them to automatically sort themselves at let's say 13:00.  I decided to do this in python as below: 

```Python
    import os
    import shutil 
    import schedule 
    import time 

    def move_files():
    # Define source directory for downloaded files
    src_dir = "C:\\Users\\User\\Downloads"

    # Define destination directories
    dst_dirs = {
        '.mp4': "C:\\Users\\User\\Videos",
        '.mp3': "C:\\Users\\User\\Music",
        '.pdf': "C:\\Users\\User\\Documents",
        '.epub': "C:\\Users\\User\\Documents",
        '.docx': "C:\\Users\\User\\Documents", 
        '.png': "C:\\Users\\User\\Pictures", 
        '.jpeg': "C:\\Users\\User\\Pictures"
    }

    # Check if the source directory exists
    if not os.path.exists(src_dir):
        print("Source directory does not exist.")
        return

    # Iterate over files in the source directory
    for file in os.listdir(src_dir):
        src_file = os.path.join(src_dir, file)
        if os.path.isfile(src_file):
            # Determine the file extension
            _, ext = os.path.splitext(file)
            # Check if the file extension matches any in the dictionary
            if ext.lower() in dst_dirs:
                # Get the destination directory based on the file extension
                dst_dir = dst_dirs[ext.lower()]
                # Create the destination directory if it doesn't exist
                if not os.path.exists(dst_dir):
                    os.makedirs(dst_dir)
                try:
                    # Move the file to the destination directory
                    shutil.move(src_file, os.path.join(dst_dir, file))
                    print(f"Moved '{file}' to '{dst_dir}'")
                except Exception as e:
                    print(f"Failed to move '{file}': {e}")

move_files() 

def job(): 
    print("Running Job...") 
    move_files() 

#Schedule the job to run daily at 13:00 hrs

schedule.every().day.at("13:00").do(job)

while True: 
    schedule.run_pending() 
    time.sleep(60) #check every minute



```