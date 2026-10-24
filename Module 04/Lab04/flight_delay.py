# Import required libraries
from pathlib import Path

import dash
import pandas as pd
import plotly.express as px
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

# Build the Dash app layout.
app.layout = html.Div(
    children=[
        html.H1(
            "Flight Delay Time Statistics",
            style={
                "textAlign": "center",
                "color": "#503D36",
                "font-size": "30px",
            },
        ),
        html.Div(
            [
                "Input Year: ",
                dcc.Input(
                    id="input-year",
                    value="2010",
                    type="number",
                    style={"height": "35px", "font-size": "30px"},
                ),
            ],
            style={"font-size": "30px"},
        ),
        html.Br(),
        html.Br(),
        # Segment 1: Carrier and Weather delay.
        html.Div(
            [
                html.Div(dcc.Graph(id="carrier-plot")),
                html.Div(dcc.Graph(id="weather-plot")),
            ],
            style={"display": "flex"},
        ),
        # Segment 2: NAS and Security delay.
        html.Div(
            [
                html.Div(dcc.Graph(id="nas-plot")),
                html.Div(dcc.Graph(id="security-plot")),
            ],
            style={"display": "flex"},
        ),
        # Segment 3: Late aircraft delay.
        html.Div(dcc.Graph(id="late-plot"), style={"width": "65%"}),
    ]
)


def compute_info(airline_data, entered_year):
    """Compute average delay dataframes for the selected year.

    Arguments:
        airline_data: Input airline data.
        entered_year: Year for which computations should be performed.

    Returns:
        Average dataframes for carrier, weather, NAS, security, and late delays.
    """
    # Select data for the entered year.
    df = airline_data[airline_data["Year"] == int(entered_year)]

    # Compute monthly delay averages by reporting airline.
    avg_car = (
        df.groupby(["Month", "Reporting_Airline"])["CarrierDelay"]
        .mean()
        .reset_index()
    )
    avg_weather = (
        df.groupby(["Month", "Reporting_Airline"])["WeatherDelay"]
        .mean()
        .reset_index()
    )
    avg_NAS = (
        df.groupby(["Month", "Reporting_Airline"])["NASDelay"]
        .mean()
        .reset_index()
    )
    avg_sec = (
        df.groupby(["Month", "Reporting_Airline"])["SecurityDelay"]
        .mean()
        .reset_index()
    )
    avg_late = (
        df.groupby(["Month", "Reporting_Airline"])["LateAircraftDelay"]
        .mean()
        .reset_index()
    )
    return avg_car, avg_weather, avg_NAS, avg_sec, avg_late


def empty_figure(title):
    """Return a blank figure when the year input is empty."""
    return px.line(title=title)


# Callback decorator: five outputs and one input.
@app.callback(
    [
        Output(component_id="carrier-plot", component_property="figure"),
        Output(component_id="weather-plot", component_property="figure"),
        Output(component_id="nas-plot", component_property="figure"),
        Output(component_id="security-plot", component_property="figure"),
        Output(component_id="late-plot", component_property="figure"),
    ],
    Input(component_id="input-year", component_property="value"),
)
def get_graph(entered_year):
    """Return the five delay figures for the selected year."""
    if entered_year in (None, ""):
        return [
            empty_figure("Average carrier delay time (minutes) by airline"),
            empty_figure("Average weather delay time (minutes) by airline"),
            empty_figure("Average NAS delay time (minutes) by airline"),
            empty_figure("Average security delay time (minutes) by airline"),
            empty_figure("Average late aircraft delay time (minutes) by airline"),
        ]

    # Compute required information for creating the graphs.
    avg_car, avg_weather, avg_NAS, avg_sec, avg_late = compute_info(
        airline_data, entered_year
    )

    # Line plot for carrier delay.
    carrier_fig = px.line(
        avg_car,
        x="Month",
        y="CarrierDelay",
        color="Reporting_Airline",
        title="Average carrier delay time (minutes) by airline",
    )

    # Line plot for weather delay.
    weather_fig = px.line(
        avg_weather,
        x="Month",
        y="WeatherDelay",
        color="Reporting_Airline",
        title="Average weather delay time (minutes) by airline",
    )

    # Line plot for NAS delay.
    nas_fig = px.line(
        avg_NAS,
        x="Month",
        y="NASDelay",
        color="Reporting_Airline",
        title="Average NAS delay time (minutes) by airline",
    )

    # Line plot for security delay.
    sec_fig = px.line(
        avg_sec,
        x="Month",
        y="SecurityDelay",
        color="Reporting_Airline",
        title="Average security delay time (minutes) by airline",
    )

    # Line plot for late aircraft delay.
    late_fig = px.line(
        avg_late,
        x="Month",
        y="LateAircraftDelay",
        color="Reporting_Airline",
        title="Average late aircraft delay time (minutes) by airline",
    )

    return [carrier_fig, weather_fig, nas_fig, sec_fig, late_fig]


# Run the app on port 8052 so earlier lab apps can remain open.
if __name__ == "__main__":
    app.run(debug=True, port=8052)
