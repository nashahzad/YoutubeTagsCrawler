# from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot, offline
# import cufflinks as cf
# import pandas as pd
from Stats import ticks, tags #, video_info
from plotly import graph_objs
from plotly.offline import plot

def draw():
    # offline.plot()
    # cf.go_offline()
    # cf.datagen.box(20).iplot(kind='box', legend=False)
    # simple_df = pd.DataFrame({'Tags': tags, 'Ticks': ticks})
    # simple_df.iplot(kind='bar')
    # d = {'creator_name': tuple([str(video[0]) for video in video_info]),
    #      'views': tuple([int(video[1]) for video in video_info]),
    #      'tags': tuple([tuple(video[2]) for video in video_info]),
    #      'date_published': tuple([str(video[3]) for video in video_info])}

    # dataframe = pd.Series(data=d)

    frame = graph_objs.Pie(labels=tags, values=ticks)

    # print("Dataframe:\n" + dataframe.describe())

    plot([frame])
