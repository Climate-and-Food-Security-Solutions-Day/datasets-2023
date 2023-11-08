# Daniel Van Hoesen
# St. Louis Neighborhoods and tracts
# display neighborhoods and tracts with overlay color for income or

############################
## Imports
############################

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.lines import Line2D
from shapely import wkt


############################
## User Variables
############################

year = 2018

file_stl_parks = 'STL_park_boundaries.csv'
dataframe_column = 'median income per household'

# Data source label
if year >= 2010:
	data_source = 'Data Source: American Community Survey'
	file = '{}_ACS_estimates_tract_population_income_boundary.csv'.format(year)
else:
	data_source = 'Data Source: U.S. Census'
	file = '{}_tract_population_income_boundary.csv'.format(year)

color_map = 'hot'


############################
## Functions
############################

def format_currency(x, pos):
	return "${:,.0f}".format(x)

############################
## Main
############################

if __name__ == "__main__":

	# initialize figure
	fig1, ax1 = plt.subplots(figsize=(6,8))
	ax1.set_axis_off()
	
	# Read the data file for the specified year containing tract, 
	# population, income, and latitude/longitude geometry
	data_csv = pd.read_csv(file)
	data = gpd.GeoDataFrame(data_csv)

	# set the tracts as the index
	data.set_index("tract", inplace=True)

	# set the geometry column to a GeoPandas geometry column
	data['geometry'] = data['geometry'].apply(wkt.loads)
	data.set_geometry('geometry', inplace=True)

	## May need to check for missing data ##
	print("\nMay need to check for missing data which could destroy the color map\n")

	# Plot data from user specified column
	data.plot(column=dataframe_column, cmap=color_map, edgecolor='black', ax=ax1, legend=False)
	
	# Read St. Louis parks geometry file
	parks_data_csv = pd.read_csv(file_stl_parks)
	parks_data = gpd.GeoDataFrame(parks_data_csv)

	# Set name as index
	parks_data.set_index("name", inplace=True)

	# Set the geometry column to a GeoPandas geometry column
	parks_data['geometry'] = parks_data['geometry'].apply(wkt.loads)
	parks_data.set_geometry('geometry', inplace=True)

	# Color parks green and the Mississippi river blue
	parks_data['color'] = 'green'
	parks_data.loc['river', 'color'] = 'blue'

	# Plot the park geometries
	parks_data.plot(color=parks_data.color, edgecolor='black', ax=ax1, linewidth=1)

	# Add Forest Park label
	ct = parks_data.loc['Forest Park'].geometry.centroid
	ax1.annotate('Forest Park', xy=(ct.x, ct.y), rotation=-6, size=9, va='center', ha='center')

	# Add custom legend for parks and no data or zero population
	custom_lines = [Line2D([0], [0], color='g', lw=10), Line2D([0], [0], color='blue', lw=10), Line2D([0], [0], color='purple', lw=10)]
	ax1.legend(custom_lines, ['Parks', 'Mississippi River', 'No data'], loc=4, frameon=False)

	# Add color bar normalized to the dataframe column specified by the user
	data_min = data[dataframe_column].min()
	data_max = data[dataframe_column].max()
	c_cor = plt.cm.ScalarMappable(cmap=color_map, norm=plt.Normalize(vmin=data_min, vmax=data_max))
	cor_bar = fig1.colorbar(c_cor, ax=ax1, shrink=0.5, format=ticker.FuncFormatter(format_currency))


	# Add figure title
	title = '{}\n{}'.format(year, dataframe_column)
	fig1.suptitle(title, x=0.5, y=0.9, fontsize=12)

	# Display data source text
	plt.gcf().text(0.2, 0.1, data_source, fontsize=12)
	
	# Show figure
	plt.show()


