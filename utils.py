from dash import dcc
from dash import html


def Header(app):
    return html.Div([get_header(app), html.Br([]), get_menu()])


def get_header(app):
    header = html.Div(
        [
            html.Div(
                
            ),
            html.Div(
                [
                    html.Div(
                        [html.H5("Credit Union Profile Report")],
                        className="seven columns main-title",
                    ),
                    html.Div(
                    ),
                ],
                className="twelve columns",
                style={"padding-left": "0"},
            ),
        ],
        className="row",
    )
    return header


def get_menu():
    menu = html.Div(
        [
            dcc.Link(
                "Overview",
                href="/overview",
                className="tab first",
            ),
            dcc.Link(
                "Peer Performance",
                href="/peer-performance",
                className="tab",
            ),
            dcc.Link(
                "Data Downloads",
                href="/downloads",
                className="tab",
            ),
        ],
        className="row all-tabs",
    )
    return menu


def make_dash_table(df):
    """ Return a dash definition of an HTML table for a Pandas dataframe """
    table = []
    for index, row in df.iterrows():
        html_row = []
        for i in range(len(row)):
            html_row.append(html.Td([row[i]]))
        table.append(html.Tr(html_row))
    return table
