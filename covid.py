import pycountry
import plotly.express as px
import pandas as pd

# ----------- Step 1 ------------
URL_DATASET = r'https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv'
df1 = pd.read_csv(URL_DATASET)
print(df1.head)  
# ----------- Step 2 ------------
list_countries = df1['Country'].unique().tolist()
print(list_countries)  
d_country_code = {}  # To hold the country names and their ISO
for country in list_countries:
    try:
        country_data = pycountry.countries.search_fuzzy(country)
        # country_data is a list of objects of class pycountry.db.Country
        country_code = country_data[0].alpha_3
        d_country_code.update({country: country_code})
    except:
        print('could not add ISO 3 code for ->', country)
        # If could not find country, make ISO code ' '
        d_country_code.update({country: ' '})

print(d_country_code)

# create a new column iso_alpha in the df
# and fill it with appropriate iso 3 code
for k, v in d_country_code.items():
    df1.loc[(df1.Country == k), 'iso_alpha'] = v


# ----------- Step 3 ------------
fig = px.choropleth(data_frame=df1,
                    locations="iso_alpha",
                    color="Confirmed",  # value in column 'Confirmed' determines color
                    hover_name="Country",
                    color_continuous_scale='RdYlGn',  #color scale red, yellow green
                    animation_frame="Date")

fig.show()
