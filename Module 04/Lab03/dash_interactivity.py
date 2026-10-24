# Import required libraries
from pathlib import Path

import dash
import pandas as pd
import plotly.graph_objects as go
from dash import dcc, html
from dash.dependencies import Input, Output

# Read the airline data into a pandas dataframe.
# Use the local Lab02 dataset when available; otherwise, use the lab URL.
DATA_URL = (
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/"
    "IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/"
    "airline_data.csv"
)
LOCAL_DATA_PATH = Path(__file__).resolve().parent.parent / "Lab02" / "airline_data.csv"
DATA_SOURCE = LOCAL_DATA_PATH if LOCAL_DATA_PATH.exists() else DATA_URL

airline_data = pd.read_csv(
    DATA_SOURCE,
    encoding="ISO-8859-1",
    dtype={
        "Div1Airport": str,
        "Div1TailNum": str,
        "Div2Airport": str,
        "Div2TailNum": str,
    },
)

# Create a Dash application.
app = dash.Dash(__name__)

# Create the application layout.
app.layout = html.Div(
    children=[
        html.H1(
            "Airline Performance Dashboard",
            style={
                "textAlign": "center",
                "color": "#503D36",
                "font-size": "40px",
            },
        ),
        html.Div(
            [
                "Input Year: ",
                dcc.Input(
                    id="input-year",
                    value="2010",
                    type="number",
                    style={"height": "50px", "font-size": "35px"},
                ),
            ],
            style={"font-size": "40px"},
        ),
        html.Br(),
        html.Br(),
        html.Div(dcc.Graph(id="line-plot")),
    ]
)


# Add the callback that updates the graph when the year changes.
@app.callback(
    Output(component_id="line-plot", component_property="figure"),
    Input(component_id="input-year", component_property="value"),
)
def get_graph(entered_year):
    """Return a line chart of average monthly arrival delay for a year."""
    if entered_year in (None, ""):
        return go.Figure().update_layout(
            title="Month vs Average Flight Delay Time",
            xaxis_title="Month",
            yaxis_title="ArrDelay",
        )

    # Select data based on the entered year.
    df = airline_data[airline_data["Year"] == int(entered_year)]

    # Group the data by month and compute the average arrival delay.
    line_data = df.groupby("Month")["ArrDelay"].mean().reset_index()

    # Create and return the line chart.
    fig = go.Figure(
        data=go.Scatter(
            x=line_data["Month"],
            y=line_data["ArrDelay"],
            mode="lines",
            marker=dict(color="green"),
        )
    )
    fig.update_layout(
        title="Month vs Average Flight Delay Time",
        xaxis_title="Month",
        yaxis_title="ArrDelay",
    )
    fig.update_xaxes(dtick=1)
    return fig


# Run the app.
if __name__ == "__main__":
    app.run(debug=True)
