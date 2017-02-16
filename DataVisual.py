import plotly
from Stats import tags, ticks
from Credentials import API_KEY, USERNAME

def draw():
    plotly.tools.set_credentials_file(username=USERNAME, api_key=API_KEY)

    frame = plotly.graph_objs.Pie(labels=tags,values=ticks)

    plotly.plotly.plot([frame])