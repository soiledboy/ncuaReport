# -*- coding: utf-8 -*-
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State 
from pages import (
    overview,
    load,
    )
from gcloud import getData
from google.cloud import bigquery
import os
from google.auth.transport import requests
import google.auth.transport.requests
import pandas as pd 
from gcloud import getData
from utils import make_dash_table
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/Users/soiledboy/dev/ncua1/hjs-376018-f51f6dec11c4.json"
app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}],
)
app.title = "Financial Report"
server = app.server

# Describe the layout/ UI of the app
app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id="page-content"),html.Div(id="result-output") ]
)

# Update page
@app.callback(Output("page-content", "children"), 
              [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/":
        return load.create_layout(app)
    
# handle form submission
@app.callback(Output('form-values-store', 'data'),
              [Input('submit-button', 'n_clicks')],
              [State('credit-union-input', 'value')])
def handle_submit(n_clicks, credit_union):
    if n_clicks > 0:
        # Store the form values in the Store component
        return {
            'credit_union': credit_union,
        }

#return data from form input 
@app.callback(Output('result-output', 'children'),
              [Input('form-values-store', 'data')])
def display_result(form_values):
    if form_values:
        # Access the form values stored in the Store component
        credit_union = form_values.get('credit_union', '')
        df = getData(credit_union)

        #cuprofile
        #row_index = 0
        #column_names = ['Charter_Number', 'CHARTER_STATE','YEAR_OPENED','PEER_GROUP','CEO','CEO_F','Acct_891']
        #cuProfile = df.loc[row_index, column_names]
        #cuProfile = cuProfile.to_frame()
        #range
        range = ['2022','2021','2020','2019']
        #totalAssets
        totalAssets = df['ACCT_010'].tolist()
        #totalLoans
        totalLoans = df['ACCT_025B'].tolist()
        #totalDeposits
        totalDeposits = df['ACCT_018'].tolist()
        #netWorth
        netWorth = df['ACCT_997'].tolist()

        return overview.create_layout(app,range,totalAssets,totalLoans,totalDeposits,netWorth)
       
        # Use the form values to display the result
        '''return html.Div(
        make_dash_table(df)
        )'''
    else:
        return ''

if __name__ == "__main__":
    app.run_server(debug=True)