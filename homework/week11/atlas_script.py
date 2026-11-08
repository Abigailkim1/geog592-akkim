# A script to display the polling places for every county in NC in a pdf. 
# Author: Abigail Kim 

print("Importing packages...")

# Importing packages
import geopandas as gpd
import matplotlib.pyplot as plt
import argparse

print("Parsing arguments...")

parser = argparse.ArgumentParser(
    description = "A program that makes an Atlas containing the polling places in NC for each county."
)
# parser.add_argument("statefp", help="The STATEFP code, for example, North Carolina is STATEFP 37")
parser.add_argument(
    ## --args default is not required 
    "--fill", type=str, default="#017aca",
    help="Number of greetings (default: blue)"
)
args = parser.parse_args()
fill = args.fill

print("Loading data...")

# Loading data 
# Source: https://www.nconemap.gov/datasets/nconemap::north-carolina-voting-polling-places/about
polling_places = gpd.read_file("North_Carolina_Voting_Polling_Places.geojson")
counties = gpd.read_file("https://www2.census.gov/geo/tiger/GENZ2024/shp/cb_2024_us_county_500k.zip")

print("Filtering and cleaning dataframes...")

# Pulling out just NC counties
nc_counties = counties.loc[counties["STATEFP"] == "37"].copy()

# Changing the CRS
ncc = nc_counties.to_crs(epsg=6543)
polling_places = polling_places.to_crs(epsg=6543)

# Filtering for only important columns. 
ncc = ncc[["GEOID", "NAME", "geometry"]]
polling_places = polling_places[["USER_pol_1", "USER_addre", "USER_city", "USER_zip","geometry"]]

# And renaming 
ncc = ncc.rename(columns={"GEOID":"geoid", "NAME":"name"})
polling_places = polling_places.rename(columns={"USER_pol_1":"poll_name", "USER_addre":"address", "USER_city":"city",
                       "USER_zip":"zip"})

print("Performing a spatial join...")

# Joining the polling places to the counties 
ncc_polls = gpd.sjoin(ncc, polling_places, predicate="contains", how="right")

# Dropping the right index 
ncc_polls = ncc_polls.drop(columns="index_left")

# Sort counties alphabetically 
ncc_polls = ncc_polls.sort_values("name").reset_index(drop=True)

print("Creating mapping functions...")

# Creating NC map with selected county highlighted.
def highlight(name, ax):
    # Pulling out just the row for that county. 
    selected = ncc[ncc["name"] == name]
    # Creating an axes object. 
    ncc.plot(ax=ax, edgecolor="grey", facecolor="white")
    # Adding an element onto that axes object. 
    selected.plot(ax=ax, edgecolor="#000000", facecolor=fill, lw=1.5)
    ax.set_axis_off()

# Map with just county.
def county_map(name, ax):
    selected = ncc[ncc["name"] == name]
    selected.plot(ax=ax, edgecolor="#000000", facecolor=fill, lw=1.5)

    # Plotting polling places 
    county_polls = ncc_polls[ncc_polls["name"] == name]
    county_polls.plot(ax=ax, color="#FFC400", markersize=20, marker="*")

    ax.set_axis_off()

# If I had more time I would write an if statement to split it into multiple pages if it's a long list. 
# A function to create each page by combining the elements.
def page(county, pdf):
    fig, axes = plt.subplots(
        2, 1,
        figsize=(8,10),
        gridspec_kw={"height_ratios": [3, 1]}
    )

    county_map(county, axes[0])
    highlight(county, axes[1])
    # TODO: Make the title bold and larger. 
    fig.suptitle(f"{county} County", fontname="Times New Roman", ha="center", va="center", fontsize=12)

    pdf.savefig(fig)
    plt.close(fig)

print("Creating a PDF...")

# Iterating through all of the counties and creating a page for each. 
from matplotlib.backends.backend_pdf import PdfPages 
with PdfPages("nc_polls_new.pdf") as pdf:  #with #manages a resource and automatically cleans up when you finish using it.
    for county in ncc["name"]:
        page(county, pdf)

print("PDF completed.")