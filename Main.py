import urllib.request, re, Stats, time, Locks, threading
from ParseCMDArgs import parse
from html.parser import HTMLParser
from DataVisual import draw
from _thread import exit as thread_exit

class Parser(HTMLParser):
    flag = False
    flagView = False
    flagTags = False
    views = 0
    tags = None

    def handle_starttag(self, tag, attrs):
        #IF HAVE TAGS AND VIEW COUNT THEN FINISH PROCESSING THIS URL/VIDEO
        if self.flagView and self.flagTags:
            self.flagView = False
            self.flagTags = False
            self.process_tags(self.tags)

        # CHECKING FOR HREF TAG FOR VIDEOS
        if tag == 'a':
            for name, value in attrs:
                if name == 'href':
                    if re.search("watch\?v=", value, flags=0):
                        Locks.urlsLock.acquire(blocking=True,timeout=-1)
                        Stats.urls.append(Stats.YOUTUBE + value)
                        Locks.urlsLock.release()

        # IF URL BEING PARSED IS YOUTUBE.COM SKIP ANY ANALYSIS ON IT
        elif threading.current_thread().name == Stats.YOUTUBE:
            return

        #CHECKING FOR KEYWORDS START TAG
        elif tag == 'meta':
            if attrs[0][0] == 'name' and attrs[0][1] == 'keywords':
                string = attrs[1][1].split(",")
                print("tags: ", string)
                self.tags = string
                self.flagTags = True

        elif tag == 'div':
            for name, value in attrs:
                if name == 'class':
                    if value == 'watch-view-count':
                        self.flag = True

    def handle_data(self, data):
        if self.flag:
            self.flag = False
            string = data.split(" ")
            string[0] = string[0].replace(",", "")
            if not string[0].isdigit():
                return
            self.views = float(string[0])
            self.flagView = True
            print(self.views)

    def process_tags(self, tags):
        Locks.tagsLock.acquire(blocking=True,timeout=-1)
        Locks.ticksLock.acquire(blocking=True,timeout=-1)

        #IF EMPTY LIST JUST DUMP IT ALL IN THERE
        if len(Stats.tags) == 0:
            for value in tags:
                Stats.tags.append(value)
                Stats.ticks.append(self.views)
            Locks.tagsLock.release()
            Locks.ticksLock.release()
        #NON-EMPTY LIST MAKE SURE TO HAVE REPEAT TAGS
        else:
            #FOR EACH NEW TAG IN NEW URL
            o = 0
            for value in tags:
                add = True
                #IF IT ALREADY EXISTS IN STATS.TAGS STATIC LIST
                #THEN DON'T ADD IT
                #OTHERWISE ADD IT
                i = 0
                for tag in Stats.tags:
                    if value == tag:
                        add = False
                        Stats.ticks[i] = Stats.ticks[i] + self.views
                    i = i + 1
                if add:
                    Stats.tags.append(value)
                    Stats.ticks.append(self.views)
                o = o + 1
            Locks.tagsLock.release()
            Locks.ticksLock.release()

class myThread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
    def run(self):
        process(self.name)


def process(url):
    # OPEN URL AND BEGIN PARSING IT
    try:
        response = urllib.request.urlopen(url)
    except:
        print("Bad url found, ending thread")
        thread_exit()
    parser = Parser()
    parser.feed(str(response.read()))


def main():
    # INITIALIZE LIST OF URLS AND TIMER
    seconds, start = parse()
    Stats.urls.append(start)
    start = time.time()
    # visited = list()
    threads = list()
    # same = 0

    # FOR CERTAIN TIME KEEP SPAWNING THREADS FOR VIDEOS
    while True:
        if time.time()-start > seconds:
            print("Time is up")
            break
        Locks.urlsLock.acquire(blocking=True,timeout=-1)
        if len(Stats.urls) == 0:
            Locks.urlsLock.release()
            continue

        url = Stats.urls.pop()
        Locks.urlsLock.release()

        # CREATE A NEW THREAD NAMED AFTER URL BEING PARSED
        t = myThread(url)
        print("Starting new thread on url: ", url)
        t.start()
        threads.append(t)


    # MAKE SURE ALL THREADS ARE JOINED AND CLEANED UP
    for t in threads:
        t.join()
    print(Stats.tags, "\n", Stats.ticks)
    draw()

main()