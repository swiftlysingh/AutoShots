import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from git import Repo
import os

class OnMyWatch:

    watchDirectory = "./Sample"

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.watchDirectory, recursive = True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Observer Stopped")

        self.observer.join()

class Handler(FileSystemEventHandler):
    @staticmethod
    def on_created(event):
        file_name = event.src_path.split("/")[-1]

        new_path = "/Users/pushpinderpalsingh/Documents/Learning/Other Projects/Python/test/images/"
        newFile = datetime.datetime.today().strftime('%H%d%m%y')+"-"+file_name

        os.rename(event.src_path,new_path + newFile)

watch = OnMyWatch()
watch.run()
