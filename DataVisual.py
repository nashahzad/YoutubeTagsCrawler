from Stats import ticks, tags, video_info
from plotly import graph_objs
from plotly.offline import plot
import matplotlib.pyplot as plt
plt.rcdefaults()
import numpy as np

def draw():

    #PIE CHART OF 30 MOST POPULAR TAGS
    pie_indeces = np.argpartition(ticks, -50)[-50:]
    pie_ticks = [int(ticks[x]) for x in pie_indeces]
    pie_tags = [str(tags[x]) for x in pie_indeces]

    frame = graph_objs.Pie(labels=pie_tags, values=pie_ticks)

    plot([frame], filename='html/YouTubeTags_PieChart.html')

    #GET THE 15 MOST POPULAR TAGS
    #GET THEIR INDECES TO ALSO GET CORRESPONDING TAG NAME
    indeces = np.argpartition(ticks, -20)[-20:]
    ticks_sub = [int(ticks[x]) for x in indeces]
    tags_sub = [str(tags[x]) for x in indeces]

    x = tags_sub
    y = ticks_sub

    data = [graph_objs.Bar(
        x=x, y=y,
        marker=dict(
            color='rgb(158,202,225)',
            line=dict(
                color='rgb(8,48,107)',
                width=1.5),
        ),
        opacity=0.6
    )]

    layout = graph_objs.Layout(
        annotations=[
            dict(x=xi, y=yi,
                 text=str(yi),
                 xanchor='center',
                 yanchor='bottom',
                 showarrow=False,
                 ) for xi, yi in zip(x, y)]
    )

    fig = graph_objs.Figure(data=data, layout=layout)
    plot(fig, filename='html/YouTubeTags_BarChart.html')

    #MAKE A VISUAL BASED ON MOST VIEWED VIDEOS
    #GRAB 15 MOST VIEWED VIDEOS
    #VIDEO_INFO: (TITLE, CREATOR, VIEWS, TAGS, DATE PUBLISHED)
    video_title, creator, views, tag, date = zip(*video_info)
    video_indeces = np.argpartition(views, -20)[-20:]
    total_views = list()
    total_tags = list()
    total_video_titles = list()

    for x in video_indeces:
        total_views.append(views[x])
        total_tags.append(tag[x])
        total_video_titles.append(video_title[x])

    c = 0
    for x in total_tags:
        total_tags[c] = ' '.join(x)
        c += 1
    trace0 = graph_objs.Bar(
        x=total_video_titles,
        y=total_views,
        text=total_tags,
        marker=dict(
            color='rgb(158,202,225)',
            line=dict(
                color='rgb(8,48,107)',
                width=1.5,
            )
        ),
        opacity=0.6
    )

    data = [trace0]
    layout = graph_objs.Layout(
        title='Most Popular Videos',
    )

    fig = graph_objs.Figure(data=data, layout=layout)
    plot(fig, filename='html/YouTubeTags_PopularVideos.html')


