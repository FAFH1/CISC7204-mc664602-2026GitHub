# Import required packages
import pandas as pd
import plotly.express as px
import dash
from dash import dcc
from dash import html

# Read the airline data into pandas dataframe
# Read the airline data into pandas dataframe
airline_data = pd.read_csv('airline_data.csv', 
                            encoding = "ISO-8859-1", 
                            dtype={'Div1Airport': str, 'Div1TailNum': str, 
                                   'Div2Airport': str, 'Div2TailNum': str})

# Randomly sample 500 data points. Setting the random state to be 42 so that we get same result.
data = airline_data.sample(n=500, random_state=42)

# Pie Chart Creation
fig = px.pie(data, values='Flights', names='DistanceGroup', title='Distance group proportion by flights')
# Create a dash application
app = dash.Dash(__name__)

# Get the layout of the application and adjust it.
# Create an outer division using html.Div and add title to the dashboard using html.H1 component
# Add description about the graph using HTML P (paragraph) component
# Finally, add graph component.
app.layout = html.Div(children=[
    # TASK 3 要求：标题文字为 'Airline Dashboard'，并设置样式
    html.H1('Airline Dashboard', 
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    # 添加描述
    html.P('Proportion of distance group by flights', 
           style={'textAlign': 'center', 'font-size': 20}),
    
    # 传入你前面定义的 fig 饼图对象
    dcc.Graph(figure=fig)
])
# Run the application
if __name__ == '__main__':
    app.run()