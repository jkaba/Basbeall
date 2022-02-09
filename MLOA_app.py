# Major League Operations Analyst Assessment
# App written in Python using Dash Framework
# Name: Jameel Kaba

# Rename file to app.py, and then run the following
# Run this app with `python app.py` and visit http://127.0.0.1:8050/ in your web browser.

# Import statements
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import flask

# Load data
df = pd.read_csv('Insert Data here')
copy_df = df

# Method to generate a table
def generate_table(dataframe, max_rows=1000):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])
    
# Release speed vs. Spin rate
# Remove release speeds of 0 due to possible error
nan_value = float("NaN")
copy_df['release_speed'].replace(0, nan_value, inplace=True)
copy_df.dropna(subset = ["events"], inplace=True)

fig_1 = px.scatter(copy_df, x="release_speed", y="release_spin_rate", color="pitcher_name", symbol="pitch_name")
                 
# Spin rate by pitch
fig_2 = px.scatter(df, x="pfx_x", y="pfx_z", color="pitcher_name", symbol="pitch_name")

# Occurrences of events based on what pitch is thrown and by whom
grouped_1 = pd.DataFrame(df.groupby(['pitcher_name','pitch_name', 'events'])['events'].count())
grouped_1.columns = ['occurences']
grouped_1.columns = grouped_1.columns.get_level_values(0)
grouped_1 = grouped_1.reset_index(level=[0,1,2])

# Occurrences of events based on balls-strikes
# Ball + Count when event occurs
# Remove all Blanks
copy_df = df
copy_df.replace("", nan_value, inplace=True)
copy_df.dropna(subset = ["events"], inplace=True)

# Reset columns to plot
grouped_2 = pd.DataFrame(copy_df.groupby(['events','balls', 'strikes'])['events'].count())
grouped_2.columns = ['occurences']
grouped_2.columns = grouped_2.columns.get_level_values(0)
grouped_2 = grouped_2.reset_index(level=[0,1,2])

fig_3 = px.scatter(grouped_2, x="strikes", y="balls", size="occurences", color="events",symbol="occurences")

# Dash Setup
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Code for each page
index_page = html.Div([
    html.H1(children='Major League Operations Analyst Assessment'),
    html.H3(children='Simple web app developed using Python Dash by Jameel Kaba'),
    html.H5(children='Below you will find links to different tables/visualizations'),
    dcc.Link('Release Speed vs. Spin Rate', href='/page-1'),
    html.Br(),
    dcc.Link('Spin Rate per Pitch', href='/page-2'),
    html.Br(),
    dcc.Link('Event Occurrences by Pitch thrown by Pitcher', href='/page-3'),
    html.Br(),
    dcc.Link('Event Occurrences by balls and strikes count', href='/page-4'),
])

page_1_layout = html.Div([
    html.H1('Release speed vs. Spin rate'),
    html.H6('Taking a look at the relationship between release speed and spin rate between pitches'),
    html.Div(id='page-1-content'),
    dcc.Graph(
        id='Pitching Data',
        figure=fig_1,
    ),
    html.Br(),
    dcc.Link('Spin Rate per Pitch', href='/page-2'),
    html.Br(),
    dcc.Link('Event Occurrences by Pitch thrown by Pitcher', href='/page-3'),
    html.Br(),
    dcc.Link('Event Occurrences by balls and strikes count', href='/page-4'),
    html.Br(),
    dcc.Link('Go back to home', href='/')
])

page_2_layout = html.Div([
    html.H1('Spin Rate per pitch'),
    html.H6('Taking a look at the movement between pitchers pitches'),
    html.Div(id='page-2-content'),
    dcc.Graph(
        id='Pitching Data',
        figure=fig_2
    ),
    html.Br(),
    dcc.Link('Release Speed vs. Spin Rate', href='/page-1'),
    html.Br(),
    dcc.Link('Event Occurrences by Pitch thrown by Pitcher', href='/page-3'),
    html.Br(),
    dcc.Link('Event Occurrences by balls and strikes count', href='/page-4'),
    html.Br(),
    dcc.Link('Go back to home', href='/')
])

page_3_layout = html.Div([
    html.Div(id='page-3-content'),
    html.H1(children='Event Occurrences by Pitch thrown by Pitcher'),
    html.Div([
        generate_table(grouped_1)
    ], className='seven columns'),
    html.Br(),
    dcc.Link('Release Speed vs. Spin Rate', href='/page-1'),
    html.Br(),
    dcc.Link('Spin Rate per Pitch', href='/page-2'),
    html.Br(),
    dcc.Link('Event Occurrences by balls and strikes count', href='/page-4'),
    html.Br(),
    dcc.Link('Go back to home', href='/'),
])

page_4_layout = html.Div([
    html.H1('Occurrences of events based on pitch count'),
    html.Div([
        html.Div(children=[
        generate_table(grouped_2)
        ], className='five columns'),
        html.Div([dcc.Graph(
        id='Pitching Data',
        figure=fig_3, className='seven columns'
        )])
    ]),
    html.Div(id='page-4-content'),
    html.Br(),
    dcc.Link('Release Speed vs. Spin Rate', href='/page-1'),
    html.Br(),
    dcc.Link('Spin by Pitch', href='/page-2'),
    html.Br(),
    dcc.Link('Event Occurrences by Pitch thrown by Pitcher', href='/page-3'),
    html.Br(),
    dcc.Link('Go back to home', href='/')
])

# Update the index
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-1':
        return page_1_layout
    elif pathname == '/page-2':
        return page_2_layout
    elif pathname == '/page-3':
        return page_3_layout
    elif pathname == '/page-4':
        return page_4_layout
    else:
        return index_page
        
if __name__ == '__main__':
    app.run_server(debug=False)
