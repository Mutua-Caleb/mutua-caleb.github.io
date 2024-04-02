---
layout: post
title: "Automatically Move files to the Right Folders"
date: 2024-04-02
---

My computer is usually a mess. When I download files from the internet, all of them go to my Windows Download folders, however when I later look at Downloads Everything looks so clunky and all gobbled up. This to be honest makes my mind not work correctly. Suprising making your digital space organised is very good for my mental health. I am trying to maintain my "digital hygiene" 

Enough with the stories. I came up with the idea that whenever I download files, let's say epub, pdf, m4a, mp3, weba files from the internet, I would like to for them to go to the respective folders. i.e epub, pdf, docx goes to C:\\Users\\User\\Documents, m4a,mp3,weba go to C:\\Users\\User\\Music, mp4 -> C:\\Users\\User\\Videos. 

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

        #Check if the source directory exists 

        if not os.path.exists(src_dir): 
            print("Source directory does not exist.")
            return 
        
        #Iterate over files in the source directory 
        for file in os.listdir(src_dir): 
            src_file = os.path.join(src_dir, file)
            if os.path.isfile(src_file): 
                #Determine the file extension
                _, ext = os.path.splitext(file) 
                if ext.lower() in dst_dirs: 
                    #Get the destination directory based on the  file extension
                    dst_dir = dst_dir[ex.lower()] 
                    #create the destination director if it doesn't exist 
                    if not os.path.exists(dst_dir): 
                        os.makedirs(dst_dir)
                    try: 
                        #move the file to the destination directory
                        shutil.move(src_file, os.path.join(dst_dir, file))
                        print(f"Moved '{file}' to '{dst_dir}'") 
                    except Exception as e: 
                        print(f"Failed to move '{file}' : {e}") 

move_files() 

def job() 
    print("Running job... ") 
    move_files() 

#Schedule the job to run daily at 13:00 hrs

schedule.every().day.at("13:17").do(job) 

while True: 
    schedule.run_pending() 
    time.sleep(60) #Check every minute



```