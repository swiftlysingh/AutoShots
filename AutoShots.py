import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from git import Repo
import os
import time
import logging

class AutoShots:
    watchDirectory = "/media/pictures/Edited/Web"

    # This will initialize the logger and oberver object
    def __init__(self):
        self.observer = Observer()
        self.logger = logging.getLogger("AutoShots")
        self.logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler('AutoShots.log')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        print("Initialized Successfully")

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.watchDirectory, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Observer Stopped")

        self.observer.join()

    # This will rename and move the file to its desired location
    def MoveFiles(self,event):
        oldFile = event.src_path.split("/")[-1]

        newFilePath = "/media/pictures/Edited/Shots/images"
        newFile = datetime.datetime.today().strftime('%S%H%d%m%y') + "-" + oldFile

        os.rename(event.src_path, newFilePath + newFile)
        self.logger.debug("Renaming and Moving Successful")

        self.updateGit(newFile)

    # This will add and update the git repo with a commit named "Update from script"
    def updateGit(self,file):
        file = "images/" + file
        repo = Repo("/media/pictures/Edited/Shots/")
        origin = repo.remote(name='origin')
        origin.pull()
        repo.index.add([file])
        repo.index.commit("Update From Script")
        origin.push()
        self.logger.debug("Pushed latest")


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_created(event):
        AutoShots().MoveFiles(event)

    @staticmethod
    def on_moved(event):
        AutoShots().MoveFiles(event)



watch = AutoShots()
watch.run()
