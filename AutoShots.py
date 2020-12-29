import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from git import Repo
import os
import time
import logging

class AutoShots:
    watchDirectory = "./Sample"

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

    def MoveFiles(self,event):
        oldFile = event.src_path.split("/")[-1]

        newFilePath = "/Users/pushpinderpalsingh/Documents/Learning/Other Projects/Python/test/images/"
        newFile = datetime.datetime.today().strftime('%S%H%d%m%y') + "-" + oldFile

        os.rename(event.src_path, newFilePath + newFile)
        self.logger.debug("Renaming and Moving Successful")

        self.updateGit(newFile)

    def updateGit(self,file):
        file = "images/" + file
        repo = Repo("/Users/pushpinderpalsingh/Documents/Learning/Other Projects/Python/test/")
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
