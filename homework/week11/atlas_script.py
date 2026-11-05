# A script to display the polling places for every county in NC in a pdf. 
# Author: Abigail Kim 

print("Importing packages...")

# Importing packages
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

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
    selected.plot(ax=ax, edgecolor="#000000", facecolor="#017aca", lw=1.5)
    ax.set_axis_off()

# Map with just county.
def county_map(name, ax):
    selected = ncc[ncc["name"] == name]
    selected.plot(ax=ax, edgecolor="#000000", facecolor="#017aca", lw=1.5)

    # Plotting polling places 
    county_polls = ncc_polls[ncc_polls["name"] == name]
    county_polls.plot(ax=ax, color="#FFC400", markersize=20, marker="*")

    ax.set_axis_off()

print("Creating a text generator function...")

# Text generator - summary of polling places. 
def summary(name): 
    county_polls = ncc_polls[ncc_polls["name"] == name]
    quantity = f"{name} County has {len(county_polls)} polling places."
    return quantity

# List of polling places by zip code as a axes object. 
def poll_addresses(zip_polls):
    text = ""
    for i in range(len(zip_polls)): 
        name = zip_polls["poll_name"].iloc[i]
        address = zip_polls["address"].iloc[i]
        poll = f"{name}, {address}\n"
        text = text + poll
    return text 


def polls_list(name, ax, x, y):
    county_polls = ncc_polls[ncc_polls["name"] == name]
    zip_codes = county_polls["zip"].unique()
    text = ""
    for i in zip_codes: 
        zip_polls = county_polls[county_polls["zip"] == i]
        addresses = poll_addresses(zip_polls)
        text = text + f"{i}\n{addresses}\n"

    ax.text(x, y, text)
    ax.set_axis_off()

print("Putting the text into an axes object...")

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

    fig.suptitle(f"{county} County", fontname="Times New Roman", ha="center", va="center", fontsize=12)
    fig.text(0.5, 0.93, summary(county), fontname="Times New Roman", ha="center", va="center", fontsize=12)

    fig2, ax = plt.subplots(figsize=(8,1))
    polls_list(county, ax, 0, 0)

    pdf.savefig(fig)
    plt.close(fig)

    pdf.savefig(fig2)
    plt.close(fig2)

print("Creating a PDF...")

# Iterating through all of the counties and creating a page for each. 
from matplotlib.backends.backend_pdf import PdfPages 
with PdfPages("nc_polls_new.pdf") as pdf:  #with #manages a resource and automatically cleans up when you finish using it.
    for county in ncc["name"]:
        page(county, pdf)

print("PDF completed.")