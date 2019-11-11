# Course project.

##  Usage :
    - You have to set the `PYTHONPATH` so your modules will be recognoized by python interpreter.
     Look into notes.txt files for details.
    -`start.py` will be our start of the script.

## Structure of the project
    - `app` will have our major code base for the project.
    - `utils` will hold all the supporting utils for our project
    - `test` has will be the place to test our new modules.
    - More chagnes as and when we move forward with other tasks.

### Completed so far:
    - Able to recognize Cone in the Video.
    - Capture Video as a proof. 
    

### Steps to Clone the Repo:
    1. Go to a folder of our choice in your pc
    2. git clone https://github.com/venkunikku/crew-2.git
    3. If id and password asked then enter your id and password for git
    4. Step#2 will checkout master repo
        5. To change branch 
        6. git fetch origin detect_drive_task1_r11102019:detect_drive_task1_r11102019
        7. git branch --set-upstream-to=origin/detect_drive_task1_r11102019 detect_drive_task1_r11102019
        8. git pull

### To commit change from your local to remote repo

    1. git status (this show all the change made in your local)
    2. git add <<path to the file>> (For example git status will give you the path to the file change. Just copy that here)
    3. git commit -m "Enter some message about your change"
    4. git push (some time if there are change in the repo that you did not pull, git push wil fail. In such cases just do git pull first and then do git push)
