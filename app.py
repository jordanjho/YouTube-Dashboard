import dash
from dash import dcc, html, Input, Output, dash_table
import pandas as pd
import plotly.express as px
from utils import tag_videos

# Load and tag data
df = pd.read_csv("data/videos.csv")
df = tag_videos(df)

app = dash.Dash(__name__)
app.title = "YouTube Channel Dashboard"

app.layout = html.Div([
    html.H2("YouTube Channel Insights"),

    html.Div([
        html.Label("Sort by:"),
        dcc.Dropdown(
            id='sort_by',
            options=[
                {'label': 'Views', 'value': 'views'},
                {'label': 'Likes', 'value': 'likes'},
                {'label': 'Title (A-Z)', 'value': 'title'},
            ],
            value='views'
        ),
        dcc.RadioItems(
            id='sort_order',
            options=[{'label': 'Descending', 'value': 'desc'}, {'label': 'Ascending', 'value': 'asc'}],
            value='desc',
            inline=True
        ),
    ], style={'width': '40%', 'display': 'inline-block'}),

    html.Div([
        html.Label("Genre:"),
        dcc.Checklist(
            id='genre-filter',
            options=[{'label': g, 'value': g} for g in sorted(df['Genre'].unique())],
            value=[c for c in sorted(df['Genre'].unique())],  # default: all selected
            inline=True
        ),
        html.Label("Animation Type:"),
        dcc.Checklist(
            id='animation-filter',
            options=[{'label': a, 'value': a} for a in sorted(df['AnimationType'].unique())],
            value=[c for c in sorted(df['AnimationType'].unique())],  # default: all selected
            inline=True
        ),
        html.Label("Content Type:"),
      dcc.Checklist(
            id='content-filter',
            options=[{'label': c, 'value': c} for c in sorted(df['ContentType'].unique())],
            value=[c for c in sorted(df['ContentType'].unique())],  # default: all selected
            inline=True
        ),
        html.Label("Copyrighted:"),
        dcc.Checklist(
            id='copyright-filter',
            options=[{'label': 'Yes', 'value': True}],
            value=[]
        ),
    ], style={'width': '55%', 'display': 'inline-block', 'verticalAlign': 'top', 'marginLeft': '2%'}),

    dcc.Graph(id='bar_chart'),

    html.Div([
        dcc.Graph(id='genre_pie_chart', style={'display': 'inline-block', 'width': '48%'}),
        dcc.Graph(id='views_time_chart', style={'display': 'inline-block', 'width': '48%'}),
    ]),

    html.H4("Video Table"),
    dash_table.DataTable(
        id='video_table',
        columns=[{"name": col, "id": col} for col in ['title', 'views', 'likes', 'Genre', 'AnimationType', 'ContentType', 'Copyrighted', 'Year']],
        data=df.to_dict('records'),
        sort_action='native',
        page_size=10,
        style_table={'overflowX': 'auto'},
    )
])

@app.callback(
    Output('bar_chart', 'figure'),
    Output('genre_pie_chart', 'figure'),
    Output('views_time_chart', 'figure'),
    Output('video_table', 'data'),
    Input('sort_by', 'value'),
    Input('sort_order', 'value'),
    Input('genre-filter', 'value'),
    Input('animation-filter', 'value'),
    Input('content-filter', 'value'),
    Input('copyright-filter', 'value')
)
def update_graphs_and_table(sort_by, sort_order, genre, animation, content, copyright_only):
    filtered = df.copy()
    if genre:
        filtered = filtered[filtered['Genre'].isin(genre)]
    if animation:
        filtered = filtered[filtered['AnimationType'].isin(animation)]
    if content:
        filtered = filtered[filtered['ContentType'].isin(content)]
    if copyright_only and True in copyright_only:
        filtered = filtered[filtered['Copyrighted'] == True]
    sorted_df = filtered.sort_values(by=sort_by, ascending=(sort_order == 'asc'))

    # Limit to top 20 for readability
    top_df = sorted_df.head(20)

    # Horizontal bar chart, hide y labels, show hover info
    bar_fig = px.bar(
        top_df,
        y='title',
        x=sort_by,
        color='Genre',
        orientation='h',
        title=f"Top 20 Videos by {sort_by.capitalize()}",
        hover_data=['title', 'views', 'likes', 'Genre', 'AnimationType', 'ContentType']
    )
    bar_fig.update_layout(
        yaxis={'visible': False, 'showticklabels': False},
        height=600
    )

    # Pie chart for Genre distribution
    pie_fig = px.pie(filtered, names='Genre', title='Genre Distribution')

    # Time series: Views over time
    if not filtered.empty:
        time_df = filtered.sort_values('published')
        time_fig = px.line(time_df, x='published', y='views', title='Views Over Time')
    else:
        time_fig = px.line(title='Views Over Time')

    return bar_fig, pie_fig, time_fig, sorted_df.to_dict('records')

if __name__ == "__main__":
    app.run(debug=True)