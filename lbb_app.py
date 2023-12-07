import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(layout='wide')

# --- READ DATA ---
customer_merge = pd.read_pickle('data/customer_merge.pkl')
coord = pd.read_csv('data/coordinate.csv')

# --- ROW 1 ---
st.write('# Customer Demography Dashboard')
st.write("""This dashboard will help us to understand more about our customers segment especially their generation class.
         This will track customer's generation proportion, customer's annual income and spendings, visualize customer distribution across provinces,
         and also customer's professions.""")

# --- ROW 2 ---
col1, col2 = st.columns(2)

## --- OVERVIEW PLOT ---

# data: overview plot
gen = pd.crosstab(index=customer_merge['generation'],
                     columns=customer_merge['gender'],
                     colnames=[None])
gen = gen.reset_index()

# plot: overview
plot_gen = px.bar(data_frame=gen,
                         x='generation', y=['Female', 'Male'],
             #labels={'value': 'Values', 'variable': 'Metric'},
             template='plotly_dark',
             barmode='group')

col1.write('### Comparison of Gender by Generation')
col1.plotly_chart(plot_gen, use_container_width=True)

### --- MAP PLOT ---
# data map
prov_generation = pd.crosstab(index=customer_merge['province'],
                              columns=customer_merge['generation'],
                              )
prov_generation['Total'] = prov_generation['Boomers']+prov_generation['Gen. X']+prov_generation['Gen. Y (Millenials)']+prov_generation['Gen. Z (Zoomers)']
df_map = prov_generation.merge(right=coord, on='province')

# plot: map
plot_map = px.scatter_mapbox(data_frame=df_map, lat='latitude', lon='longitude',
                             mapbox_style='carto-positron', zoom=3,
                             size='Total',
                             hover_name='province',
                             hover_data={'Boomers': True,
                                         'Gen. X': True,
                                         'Gen. Y (Millenials)': True,
                                         'Gen. Z (Zoomers)': True,
                                         'latitude': False,
                                         'longitude': False})
col2.write('### Customer\'s Generation Across Indonesia')
col2.plotly_chart(plot_map, use_container_width=True)


# ---ROW 3 ---
st.divider()
col3, col4 = st.columns(2)

# --- input select ---
input_select = col3.selectbox(
    label='Select Gender',
    options=customer_merge['gender'].unique().sort_values()
)

col4.write('##### Use the dropdown menu on the side to see comparisons by gender on the chart below')

# --- ROW 4 ---
st.divider()
col5, col6 = st.columns(2)


### --- PLOT GEN INCOME
# data gen income
cust_gender = customer_merge[customer_merge['gender'] == input_select]
gen_income = cust_gender.groupby('generation')[['Annual_Income', 'Spending_Score']].mean()
gen_income = gen_income.reset_index()
gen_income['Annual_Income'] = gen_income['Annual_Income']/1000000

# plot gen income
plot_gen_income = px.bar(data_frame=gen_income,
                         x='generation', y=['Annual_Income', 'Spending_Score'],
             labels={'value': 'Average Income (million) & Spending Score', 
                     'variable': 'Metric',
                     'generation' : 'Generation'},
             template='plotly_dark',
             barmode='group')

col5.write(f'### Comparison of {input_select} Customer Average Annual Income and Spending Score by Generation (In Million)' )
col5.plotly_chart(plot_gen_income, use_container_width=True)

### --- PROFESSION PLOT ---
# profession data
profes_gender = customer_merge[customer_merge['gender'] == input_select]

profession_gen = pd.crosstab(index=profes_gender['Profession'],
                             columns = customer_merge['generation'],
                             colnames=[None])
melt_gen_profession = profession_gen.melt(ignore_index=False, var_name='generation', value_name='num_people')
melt_gen_profession = melt_gen_profession.reset_index()


# plot gen profession
plot_profession = px.bar(data_frame=melt_gen_profession.sort_values(by='num_people'), 
                   x='num_people', y='Profession', color='generation', barmode='group',
                   labels={'num_people': 'Profession Count',
                            'Profession': 'Profession',
                            'generation': 'Generation'},
                    category_orders={'generation': ['Boomers', 'Gen. X', 'Gen. Y (Millenials)', 'Gen. Z (Zoomers)']})

col6.write(f'### {input_select} Customer Profession Comparison by Generation' )
col6.plotly_chart(plot_profession, use_container_width=True)