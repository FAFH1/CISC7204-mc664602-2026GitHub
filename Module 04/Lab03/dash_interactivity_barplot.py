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

# Create the application layout.
app.layout = html.Div(
    children=[
        html.H1(
            "Total number of flights to the destination state split by reporting airline",
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
        html.Div(dcc.Graph(id="bar-plot")),
    ]
)


# Add the callback that updates the bar chart when the year changes.
@app.callback(
    Output(component_id="bar-plot", component_property="figure"),
    Input(component_id="input-year", component_property="value"),
)
def get_graph(entered_year):
    """Return total flights by destination state and reporting airline."""
    if entered_year in (None, ""):
        return px.bar().update_layout(
            title="Flights to Destination State",
            xaxis_title="DestState",
            yaxis_title="Flights",
        )

    # Select data based on the entered year.
    df = airline_data[airline_data["Year"] == int(entered_year)]

    # Compute the total number of flights for each destination state.
    bar_data = df.groupby("DestState")["Flights"].sum().reset_index()

    # Create the bar chart.
    fig = px.bar(
        bar_data,
        x="DestState",
        y="Flights",
        title=(
            "Total number of flights to the destination state "
            "split by reporting airline"
        ),
    )
    fig.update_layout(
        title="Flights to Destination State",
        xaxis_title="DestState",
        yaxis_title="Flights",
    )
    return fig


# Run the app on port 8051 because the line-chart app uses 8050.
if __name__ == "__main__":
    app.run(debug=True, port=8051)
