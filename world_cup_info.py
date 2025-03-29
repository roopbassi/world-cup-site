#!/usr/bin/env python
# coding: utf-8

# In[25]:


import pandas as pd
from dash import dash, html, dcc, Input, Output
import plotly.express as px
import plotly.graph_objects as go


# In[46]:


# Step 1 Create Dataframe

df = pd.DataFrame({

    'Winners': ['Uruguay', 'Italy', 'Italy', 'Uruguay', 'Germany', 'Brazil', 'Brazil', 'England', 'Brazil', 'Germany', 'Argentina', 'Italy', 'Argentina', 'Germany', 'Brazil', 'France', 'Brazil', 'Italy', 'Spain', 'Germany', 'France', 'Argentina'],
    'Runners': ['Argentina', 'Czechoslovakia', 'Hungary', 'Brazil', 'Hungary', 'Sweden', 'Czechoslovakia', 'Germany', 'Italy', 'Netherlands', 'Netherlands', 'Germany', 'Germany', 'Argentina', 'Italy', 'Brazil', 'Germany', 'France', 'Netherlands', 'Argentina', 'Croatia', 'France'],
    'Year': ['1930', '1934', '1938', '1950', '1954', '1958', '1962', '1966', '1970', '1974', '1978', '1982', '1986', '1990', '1994', '1998', '2002', '2006', '2010', '2014', '2018', '2022']
})


# Step 2

fig = px.choropleth(
    df,
    locations="Winners",
    locationmode = "country names",
    color="Winners",
    color_continuous_scale='Viridis',
    scope="world",
    title="World Cup Winners"
)
fig.update_geos(showcountries=True, showcoastlines=True, showland=True, fitbounds="geojson")

countries = []
for i,r in df.iterrows():
    for col in df.columns:
        if r[col] not in countries and r[col][0] != '1' and r[col][0] != '2':
            countries.append(r[col])

years = []
for i,r in df.iterrows():
    for col in df.columns:
        if r[col][0] == '1' or r[col][0] == '2':
            years.append(r[col])


app = dash.Dash(__name__)

server = app.server

app.layout = [
    html.H1(children="World Cup Information", style={'textAlign': 'center'}),
    dcc.Graph(figure=fig),

    html.H2(children="View The Amount of Times a Country Has Won"),
    dcc.Dropdown(options=countries, id="dropdown"),
    dcc.Graph(id="wins"),
    html.H2(id="text"),

    html.H2(children='Select Year To see World Cup Winner and Runner-Up'),
    dcc.Dropdown(options=years, id="year-dropdown"),
    dcc.Graph(id="year-winner"),
    html.H2(id="text2")
]

@app.callback(
    [Output('wins', 'figure'), Output('text', 'children'), Output('year-winner', 'figure'), Output('text2', 'children')],
    [Input('dropdown', 'value'), Input('year-dropdown', 'value')]
)

def update_graph(country, year):

    totalWins = df['Winners'].value_counts().get(country, 0)
    countriesWins = df['Winners'].value_counts().reset_index()

    text = f"{country} has won {totalWins} World Cup(s)!"
    
    fig = px.choropleth(
        countriesWins,
        locations="Winners",
        locationmode = "country names",
        color="count",
        color_continuous_scale='Viridis',
        title="World Cup Wins"
    )
    fig.update_geos(showcountries=True, showcoastlines=True, showland=True, fitbounds="geojson")


    index = df.index[df["Year"] == year]
    winner = df["Winners"].values[index]
    runner = df["Runners"].values[index]
    
    fig2 = px.choropleth(
        countriesWins,
        locations="Winners",
        locationmode = "country names",
        color="count",
        color_continuous_scale='Viridis',
        title="World Cup Winners"
    )
    fig2.update_geos(showcountries=True, showcoastlines=True, showland=True, fitbounds="geojson")

    text2 = f"Year {year}, Winners: {winner} and Runners: {runner}"
    
    return fig, text, fig2, text2

if __name__ == '__main__':
    app.run(debug=True)


# In[ ]:




