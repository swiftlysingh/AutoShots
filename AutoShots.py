import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from git import Repo
import os
import time
import asyncio

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
        asyncio.run(MoveFiles(event))


    @staticmethod
    def on_moved(event):
        asyncio.run(MoveFiles(event))


async def MoveFiles(event):
    file_name = event.src_path.split("/")[-1]

    new_path = "/Users/pushpinderpalsingh/Documents/Learning/Other Projects/Python/test/images/"
    newFile = datetime.datetime.today().strftime('%H%d%m%y') + "-" + file_name

    os.rename(event.src_path, new_path + newFile)
    print("Renaming and Moving Successful")

    await asyncio.sleep(1)

    asyncio.run(updateGit(newFile))

async def updateGit(file):
    repo = Repo("/Users/pushpinderpalsingh/Documents/Learning/Other Projects/Python/test")
    origin = repo.remote(name='origin')
    origin.pull()
    repo.index.add([file])
    repo.index.commit("Update From Script")
    origin.push()


watch = OnMyWatch()
watch.run()