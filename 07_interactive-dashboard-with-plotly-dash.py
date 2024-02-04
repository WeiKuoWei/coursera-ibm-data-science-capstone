import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("datasets/spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                             options=[
                                                 {'label': 'All Sites', 'value': 'ALL'},
                                                 {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                 {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                 {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                 {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
                                             ],
                                             value='ALL',
                                             placeholder="Select a Launch Site",
                                             searchable=True
                                             ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),

                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=min_payload,
                                                max=max_payload,
                                                step=1000,
                                                # convert min_payload to int to avoid error
                
                                                marks={i: str(i) for i in range(int(min_payload), int(max_payload) + 1000, 1000)},
                                                value=[min_payload, max_payload]
                                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])


# Callback function to update pie chart based on dropdown selection
@app.callback(Output('success-pie-chart', 'figure'),
              [Input('site-dropdown', 'value')])
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        pie_chart_data = spacex_df.groupby('class')['class'].count().reset_index(name='count')
        title = 'Total Success Launches by Site'
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        pie_chart_data = filtered_df.groupby('class')['class'].count().reset_index(name='count')
        title = f'Success vs. Failed Launches for {selected_site}'

    pie_chart_fig = px.pie(pie_chart_data, values='count', names='class', title=title)
    return pie_chart_fig


# Callback function to update scatter chart based on slider selection
@app.callback(Output('success-payload-scatter-chart', 'figure'),
              [Input('site-dropdown', 'value'),
               Input('payload-slider', 'value')])
def update_scatter_chart(selected_site, payload_range):
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
                             (spacex_df['Payload Mass (kg)'] <= payload_range[1])]
    if selected_site == 'ALL':
        scatter_chart_fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category',
                                       title='Correlation between Payload and Launch Success for All Sites')
    else:
        filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]
        scatter_chart_fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category',
                                       title=f'Correlation between Payload and Launch Success for {selected_site}')

    return scatter_chart_fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
