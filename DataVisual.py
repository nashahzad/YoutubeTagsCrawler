from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly
import pandas as pd
from Stats import tags, ticks, video_info
from sklearn.cluster import KMeans

def draw():
    d = {'creator_name':tuple([str(video[0]) for video in video_info]),
         'views':tuple([int(video[1]) for video in video_info]),
         'tags':tuple([tuple(video[2]) for video in video_info]),
         'date_published':tuple([str(video[3]) for video in video_info])}

    dataframe = pd.Series(data=d)

    frame = plotly.graph_objs.Pie(labels=tags,values=ticks)

    print("Dataframe:\n" + dataframe.describe())

    plot([frame])
