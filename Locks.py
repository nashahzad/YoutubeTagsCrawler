import threading

tagsLock = threading.Lock()
ticksLock = threading.Lock()
urlsLock = threading.Lock()

video_info = threading.Lock()