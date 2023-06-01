import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import tkinter as tk
from tkinter import messagebox
import dash_bootstrap_components as dbc
import webbrowser

def callback(url):
    webbrowser.open_new(url)

def popup_msg():
    # create a top level widget
    win = tk.Toplevel()
    win.wm_title("Notification")

    msg = "Visualization is ready. Please "
    link = "click here"
    end_msg = " to view."

    # Set up message with hyperlink
    msg_label = tk.Label(win, text=msg, font=("Arial", 16))
    link_label = tk.Label(win, text=link, fg="blue", cursor="hand2", font=("Arial", 16))  # Change the font size here
    end_msg_label = tk.Label(win, text=end_msg, font=("Arial", 16))

    msg_label.pack(side="left")
    link_label.pack(side="left")
    end_msg_label.pack(side="left")

    link_label.bind("<Button-1>", lambda e: callback("http://localhost:8050"))

df = pd.read_csv("data.csv")
df.dropna(how='all', inplace=True)
# Plot and display an interactive visualisation of bar to pie charts.
def make_interactive_pie_bar(df):
    category1 = 'Classification'
    category2 = 'Location'
    subcategory1 = 'SubClassification'
    subcategory2 = 'SubClassification'
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])

    app.layout = html.Div([
        html.Br(),
        html.H2('\nWelcome to an interactive data experience', style={'textAlign': 'center', 'font-family': 'Arial'}),
        html.Br(),
        html.P('On this page you may interact with visualisations extracted from data of job postings on seek.com\n', style={'textAlign': 'center', 'font-family': 'Arial'}),
        # First section
        html.Br(),
        html.H3('Job Classification & SubClassification', style={'textAlign': 'center', 'font-family': 'Arial'}),
        html.P('click on a pie wedge you would like to investigate and the subclassifications will be displayed.', style={'textAlign': 'center', 'font-family': 'Arial'}),
        dcc.Graph(id='pie-chart-1', 
                figure=go.Figure(data=[go.Pie(labels=df[category1].value_counts().index.tolist(),
                                                values=df[category1].value_counts().values.tolist())])
                            .update_layout(height=600, width=1200)),

        dcc.Graph(id='bar-chart-1'),
        # Second section
        html.H3('Locations and SubClassifications', style={'textAlign': 'center', 'font-family': 'Arial'}),
        html.P('click on a pie wedge you would like to investigate and the subclassifications will be displayed.', style={'textAlign': 'center', 'font-family': 'Arial'}),
        dcc.Graph(id='pie-chart-2', 
                figure=go.Figure(data=[go.Pie(labels=df[category2].value_counts().index.tolist(),
                                                values=df[category2].value_counts().values.tolist(),
                                                textinfo='none')])
                            .update_layout(height=600, width=1200)),

        dcc.Graph(id='bar-chart-2')
    ])

    @app.callback(
        Output('bar-chart-1', 'figure'),
        Input('pie-chart-1', 'clickData'))
    def update_bar_chart_1(clickData):
        if clickData is None:
            slice = 'Hospitality & Tourism'
        else:
            slice = clickData['points'][0]['label']
        ratios = df[df[category1] == slice][subcategory1].value_counts(normalize=True).values.tolist()
        labels = df[df[category1] == slice][subcategory1].value_counts(normalize=True).index.tolist()
        fig = go.Figure(data=[go.Bar(x=labels, y=ratios)]).update_layout(title_text=slice)
        fig.update_yaxes(tickformat=".0%")
        return fig

    @app.callback(
        Output('bar-chart-2', 'figure'),
        Input('pie-chart-2', 'clickData'))
    def update_bar_chart_2(clickData):
        if clickData is None:
            slice = 'Sydney'
        else:
            slice = clickData['points'][0]['label']
        ratios = df[df[category2] == slice][subcategory2].value_counts(normalize=True).values.tolist()
        labels = df[df[category2] == slice][subcategory2].value_counts(normalize=True).index.tolist()
        fig = go.Figure(data=[go.Bar(x=labels, y=ratios)])
        fig.update_layout(title_text=slice)
        fig.update_yaxes(tickformat=".0%")
        return fig

    return app
print('interactive.py loaded')
popup_msg()
tk.mainloop()

if __name__ == '__main__':
    app = make_interactive_pie_bar(df)
    app.run_server(debug=True, use_reloader=False)
