import urllib.request, re, Stats, time, Locks, threading
from html.parser import HTMLParser

class Parser(HTMLParser):
    flag = False
    flagView = False
    flagTags = False
    views = 0
    tags = None

    def handle_starttag(self, tag, attrs):
        #CHECKING FOR HREF TAG FOR VIDEOS
        if self.flagView and self.flagTags:
            self.flagView = False
            self.flagTags = False
            self.process_tags(self.tags)
        if tag == 'a':
            for name, value in attrs:
                if name == 'href':
                    if re.search("watch\?v=", value, flags=0):
                        Locks.urlsLock.acquire()
                        Stats.urls.append(Stats.YOUTUBE + value)
                        Locks.urlsLock.release()
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
        Locks.tagsLock.acquire()
        Locks.ticksLock.acquire()

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
    # print("Opening ", url)
    response = urllib.request.urlopen(url)
    parser = Parser()
    parser.feed(str(response.read()))


def main():
    # response = urllib.request.urlopen("http://youtube.com");
    Stats.urls.append(Stats.YOUTUBE)
    start = time.time()
    visited = list()
    threads = list()
    while True:
        if time.time()-start > 60:
            print("Time is up")
            break
        if len(Stats.urls) == 0:
            for t in threads:
                t.join()
        url = Stats.urls.pop()

        #CHECK FOR DUPLICATE URLS
        visited.append(url)
        if len(visited) != len(set(visited)):
            continue

        t = myThread(url)
        print("Starting new thread on url: ", url)
        t.start()
        threads.append(t)



    print(Stats.tags, "\n", Stats.ticks)

main();