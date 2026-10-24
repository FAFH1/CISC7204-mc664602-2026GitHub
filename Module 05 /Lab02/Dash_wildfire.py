# Import required libraries
from pathlib import Path

import dash
import pandas as pd
import plotly.express as px
from dash import Input, Output, dcc, html

# Create the Dash application.
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True

# Read the wildfire dataset.
DATA_URL = (
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/"
    "IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/"
    "Historical_Wildfires.csv"
)
LOCAL_DATA_PATH = Path(__file__).resolve().parent / "Historical_Wildfires.csv"
DATA_SOURCE = LOCAL_DATA_PATH if LOCAL_DATA_PATH.exists() else DATA_URL

try:
    df = pd.read_csv(DATA_SOURCE)
except Exception:
    # Fall back to the public lab dataset if the local copy is unavailable.
    df = pd.read_csv(DATA_URL)

# Extract year and month from the date column.
df["Month"] = pd.to_datetime(df["Date"]).dt.month_name()
df["Year"] = pd.to_datetime(df["Date"]).dt.year

# Build the dashboard layout.
app.layout = html.Div(
    children=[
        html.H1(
            "Australia Wildfire Dashboard",
            style={
                "textAlign": "center",
                "color": "#503D36",
                "font-size": "26px",
            },
        ),
        html.Div(
            [
                # Region selection.
                html.Div(
                    [
                        html.H2("Select Region:", style={"margin-right": "2em"}),
                        dcc.RadioItems(
                            [
                                {"label": "New South Wales", "value": "NSW"},
                                {"label": "Northern Territory", "value": "NT"},
                                {"label": "Queensland", "value": "QL"},
                                {"label": "South Australia", "value": "SA"},
                                {"label": "Tasmania", "value": "TA"},
                                {"label": "Victoria", "value": "VI"},
                                {"label": "Western Australia", "value": "WA"},
                            ],
                            value="NSW",
                            id="region",
                            inline=True,
                        ),
                    ]
                ),
                # Year selection.
                html.Div(
                    [
                        html.H2(
                            "Select Year:",
                            style={"margin-right": "2em"},
                        ),
                        dcc.Dropdown(
                            sorted(df["Year"].dropna().unique().tolist()),
                            value=2005,
                            id="year",
                        ),
                    ]
                ),
                # Output charts.
                html.Div(
                    [
                        html.Div([], id="plot1"),
                        html.Div([], id="plot2"),
                    ],
                    style={"display": "flex"},
                ),
            ],
            style={"padding": "20px"},
        ),
    ]
)


@app.callback(
    [
        Output(component_id="plot1", component_property="children"),
        Output(component_id="plot2", component_property="children"),
    ],
    [
        Input(component_id="region", component_property="value"),
        Input(component_id="year", component_property="value"),
    ],
)
def reg_year_display(input_region, input_year):
    """Create the two wildfire charts for the selected region and year."""
    region_data = df[df["Region"] == input_region]
    y_r_data = region_data[region_data["Year"] == input_year]

    # Monthly average estimated fire area.
    est_data = (
        y_r_data.groupby("Month")["Estimated_fire_area"]
        .mean()
        .reset_index()
    )
    fig1 = px.pie(
        est_data,
        values="Estimated_fire_area",
        names="Month",
        title="{} : Monthly Average Estimated Fire Area in year {}".format(
            input_region, input_year
        ),
    )

    # Monthly average count of pixels for presumed vegetation fires.
    veg_data = y_r_data.groupby("Month")["Count"].mean().reset_index()
    fig2 = px.bar(
        veg_data,
        x="Month",
        y="Count",
        title=(
            "{} : Average Count of Pixels for Presumed Vegetation Fires "
            "in year {}"
        ).format(input_region, input_year),
    )

    return [dcc.Graph(figure=fig1), dcc.Graph(figure=fig2)]


if __name__ == "__main__":
    # Use port 8053 to avoid conflicts with the earlier lab applications.
    app.run(debug=True, port=8054)
