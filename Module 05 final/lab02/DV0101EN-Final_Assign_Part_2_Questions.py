"""Automobile Sales Statistics Dashboard.

Final Project - Part 02: Creating Dashboard with Plotly and Dash.
"""

from pathlib import Path

import dash
import pandas as pd
import plotly.express as px
from dash import Input, Output, dcc, html

# Load the dataset, using a local copy when available.
DATA_URL = (
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/"
    "d51iMGfp_t0QpO30Lym-dw/automobile-sales.csv"
)
LOCAL_DATA_PATH = Path(__file__).resolve().parent / "automobile-sales.csv"
DATA_SOURCE = LOCAL_DATA_PATH if LOCAL_DATA_PATH.exists() else DATA_URL
data = pd.read_csv(DATA_SOURCE)

# Ensure month names display in calendar order.
MONTH_ORDER = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
]

# Initialize the Dash application.
app = dash.Dash(__name__)
app.title = "Automobile Statistics Dashboard"

# Dropdown options and year list.
dropdown_options = [
    {"label": "Yearly Statistics", "value": "Yearly Statistics"},
    {"label": "Recession Period Statistics", "value": "Recession Period Statistics"},
]
year_list = list(range(1980, 2024))

# Build the application layout.
app.layout = html.Div(
    [
        # TASK 2.1: Dashboard title.
        html.H1(
            "Automobile Sales Statistics Dashboard",
            style={
                "textAlign": "center",
                "color": "#503D36",
                "font-size": "24px",
            },
        ),
        # TASK 2.2: Report type dropdown.
        html.Div(
            [
                html.Label("Select Statistics:"),
                dcc.Dropdown(
                    id="dropdown-statistics",
                    options=dropdown_options,
                    value="Select Statistics",
                    placeholder="Select a report type",
                    style={
                        "width": "80%",
                        "padding": "3px",
                        "font-size": "20px",
                        "text-align-last": "center",
                    },
                ),
            ]
        ),
        # TASK 2.2: Year dropdown.
        html.Div(
            [
                html.Label("Select Year:"),
                dcc.Dropdown(
                    id="select-year",
                    options=[{"label": year, "value": year} for year in year_list],
                    value="Select-year",
                    placeholder="Select-year",
                    style={
                        "width": "80%",
                        "padding": "3px",
                        "font-size": "20px",
                        "text-align-last": "center",
                    },
                ),
            ]
        ),
        # TASK 2.3: Output container for the four charts.
        html.Div(
            [
                html.Div(
                    id="output-container",
                    className="chart-grid",
                    style={"display": "flex", "flex-wrap": "wrap"},
                ),
            ]
        ),
    ],
    style={"padding": "20px"},
)


# TASK 2.4: Enable the year dropdown only for yearly statistics.
@app.callback(
    Output(component_id="select-year", component_property="disabled"),
    Input(component_id="dropdown-statistics", component_property="value"),
)
def update_input_container(selected_statistics):
    if selected_statistics == "Yearly Statistics":
        return False
    return True


def chart_row(*charts):
    """Return one row containing two equally sized chart containers."""
    return html.Div(
        className="chart-item",
        children=[
            html.Div(children=chart, style={"width": "50%"})
            for chart in charts
        ],
        style={"display": "flex", "width": "100%"},
    )


# TASK 2.5 and TASK 2.6: Update the four output charts.
@app.callback(
    Output(component_id="output-container", component_property="children"),
    [
        Input(component_id="dropdown-statistics", component_property="value"),
        Input(component_id="select-year", component_property="value"),
    ],
)
def update_output_container(selected_statistics, input_year):
    if selected_statistics == "Recession Period Statistics":
        recession_data = data[data["Recession"] == 1]

        # Plot 1: Average yearly sales during recessions.
        yearly_rec = (
            recession_data.groupby("Year")["Automobile_Sales"]
            .mean()
            .reset_index()
        )
        R_chart1 = dcc.Graph(
            figure=px.line(
                yearly_rec,
                x="Year",
                y="Automobile_Sales",
                title="Average Automobile Sales Fluctuation over Recession Period",
            )
        )

        # Plot 2: Average vehicles sold by vehicle type during recessions.
        average_sales = (
            recession_data.groupby("Vehicle_Type")["Automobile_Sales"]
            .mean()
            .reset_index()
        )
        R_chart2 = dcc.Graph(
            figure=px.bar(
                average_sales,
                x="Vehicle_Type",
                y="Automobile_Sales",
                title=(
                    "Average Number of Vehicles Sold by Vehicle Type "
                    "during Recessions"
                ),
            )
        )

        # Plot 3: Advertising expenditure share by vehicle type.
        exp_rec = (
            recession_data.groupby("Vehicle_Type")["Advertising_Expenditure"]
            .sum()
            .reset_index()
        )
        R_chart3 = dcc.Graph(
            figure=px.pie(
                exp_rec,
                values="Advertising_Expenditure",
                names="Vehicle_Type",
                title=(
                    "Total Expenditure Share by Vehicle Type "
                    "during Recessions"
                ),
            )
        )

        # Plot 4: Effect of unemployment rate on sales by vehicle type.
        unemp_data = (
            recession_data.groupby(
                ["unemployment_rate", "Vehicle_Type"], as_index=False
            )["Automobile_Sales"]
            .mean()
        )
        R_chart4 = dcc.Graph(
            figure=px.bar(
                unemp_data,
                x="unemployment_rate",
                y="Automobile_Sales",
                color="Vehicle_Type",
                labels={
                    "unemployment_rate": "Unemployment Rate",
                    "Automobile_Sales": "Average Automobile Sales",
                },
                title="Effect of Unemployment Rate on Vehicle Type and Sales",
            )
        )

        return [
            chart_row(R_chart1, R_chart2),
            chart_row(R_chart3, R_chart4),
        ]

    if (
        selected_statistics == "Yearly Statistics"
        and input_year not in (None, "Select-year")
    ):
        yearly_data = data[data["Year"] == int(input_year)]

        # Plot 1: Yearly average sales for the whole period.
        yas = (
            data.groupby("Year")["Automobile_Sales"].mean().reset_index()
        )
        Y_chart1 = dcc.Graph(
            figure=px.line(
                yas,
                x="Year",
                y="Automobile_Sales",
                title="Yearly Automobile Sales",
            )
        )

        # Plot 2: Total monthly sales for the selected year.
        mas = (
            yearly_data.groupby("Month")["Automobile_Sales"]
            .sum()
            .reset_index()
        )
        mas["Month"] = pd.Categorical(
            mas["Month"], categories=MONTH_ORDER, ordered=True
        )
        mas = mas.sort_values("Month")
        Y_chart2 = dcc.Graph(
            figure=px.line(
                mas,
                x="Month",
                y="Automobile_Sales",
                title="Total Monthly Automobile Sales",
            )
        )

        # Plot 3: Average vehicles sold by type in the selected year.
        avr_vdata = (
            yearly_data.groupby("Vehicle_Type")["Automobile_Sales"]
            .mean()
            .reset_index()
        )
        Y_chart3 = dcc.Graph(
            figure=px.bar(
                avr_vdata,
                x="Vehicle_Type",
                y="Automobile_Sales",
                title=(
                    "Average Vehicles Sold by Vehicle Type "
                    f"in the year {input_year}"
                ),
            )
        )

        # Plot 4: Advertising expenditure by vehicle type in the selected year.
        exp_data = (
            yearly_data.groupby("Vehicle_Type")["Advertising_Expenditure"]
            .sum()
            .reset_index()
        )
        Y_chart4 = dcc.Graph(
            figure=px.pie(
                exp_data,
                values="Advertising_Expenditure",
                names="Vehicle_Type",
                title=(
                    "Total Advertisement Expenditure for Each Vehicle "
                    f"in the year {input_year}"
                ),
            )
        )

        return [
            chart_row(Y_chart1, Y_chart2),
            chart_row(Y_chart3, Y_chart4),
        ]

    return html.Div(
        "Please select a report type. For Yearly Statistics, also select a year.",
        style={"padding": "20px", "font-size": "18px"},
    )


if __name__ == "__main__":
    # Use port 8055 to avoid conflicts with earlier lab applications.
    app.run(debug=True, port=8056)
