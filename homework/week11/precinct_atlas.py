print("Importing packages")

import geopandas as gpd
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser(
    description = "A program that makes an Atlas containing the polling places for each precinct in an NC county."
)
# parser.add_argument("statefp", help="The STATEFP code, for example, North Carolina is STATEFP 37")
parser.add_argument(
    "county", 
    help="The county to create the atlas for. Input the county name, capitalized. For example, 'Wake'."
)
parser.add_argument(
    ## --args default is not required 
    "--fill", type=str, default="#017aca",
    help="Map fill color (default: blue)"
)
parser.add_argument(
    "--filename", 
    type=str,
    default="county_polls.pdf",
    help="Name of the file"
)
args = parser.parse_args()
county = args.county
fill = args.fill
filename = args.filename

print("Loading data")

# Loading data
# The precinct data is from 2026 and the polls data is from 2020 so there are some errors.
# Source: https://www.nconemap.gov/datasets/nconemap::north-carolina-voting-precincts/about 
all_precincts = gpd.read_file("Voting_Precincts.geojson")
# Source: https://www.nconemap.gov/datasets/nconemap::north-carolina-voting-polling-places/about 
polls = gpd.read_file("North_Carolina_Voting_Polling_Places.geojson")

# Selecting only the columns needed from each dataframe. 
polls = polls[["USER_pol_1", "USER_addre", "USER_city", "USER_zip","geometry"]]
all_precincts = all_precincts[["prec_id", "county_nam", "geometry"]]

# And renaming 
polls = polls.rename(columns={"USER_pol_1":"poll_name", "USER_addre":"address", "USER_city":"city",
                       "USER_zip":"zip"})
all_precincts = all_precincts.rename(columns={"county_nam":"county"})

# Formatting the county column 
all_precincts["county"] = all_precincts["county"].str.capitalize()

# Selecting just the precincts for one county. 
precincts = all_precincts[all_precincts["county"] == county].copy()

# Changing the CRS
precincts = precincts.to_crs(epsg=6543)
polls = polls.to_crs(epsg=6543)

# Process
# Let the user pick one county 
# Join the polls to the precincts 
# Then select the precincts that match the county the user inputs
# Iterate through each precinct to show on the map 
# for precinct in prec_id:
#     make a page 

print("Executing a spatial join")

# Joining the precinct data to the polls. 
polls_join = gpd.sjoin(polls, precincts, predicate="intersects")
polls_join = polls_join.drop(columns="index_right")

# Creating a function with name as an argument.
# Will later iterate through filling in prec_id.

# Creating function for county map with the precinct highlighted. 
def highlight(name, ax): 
    selected = precincts[precincts["prec_id"] == name]
    precincts.plot(ax=ax, edgecolor="grey", facecolor="white")
    selected.plot(ax=ax, edgecolor="#000000", facecolor=fill, lw=1.5)
    ax.set_axis_off()

# Map with just precinct.
def precinct_map(name, ax):
    selected = precincts[precincts["prec_id"] == name]
    selected.plot(ax=ax, edgecolor="#000000", facecolor=fill, lw=1.5)

    # Plotting polling places 
    precinct_poll = polls_join[polls_join["prec_id"] == name]
    if len(precinct_poll) > 0:
        precinct_poll.plot(ax=ax, color="#FFC400", markersize=70, marker="*")

    ax.set_axis_off()

def summary(name):
    row = polls_join[polls_join["prec_id"] == name]
    if len(row) > 0: 
        poll_address = row["address"].iloc[0]
        text = f"Poll address: {poll_address}"
    else: 
        text = "No poll"
    return text 

print("Function to create each page")

# A function to create each page by combining the elements.
def page(precinct, pdf):
    fig, axes = plt.subplots(
        2, 1,
        figsize=(8,10),
        gridspec_kw={"height_ratios": [3, 1]}
    )

    precinct_map(precinct, axes[0])
    highlight(precinct, axes[1])

    fig.suptitle(f"Precinct {precinct}", 
                 fontname="Times New Roman", 
                 ha="center", va="center", 
                 fontsize=18, 
                 fontweight="bold")
    fig.text(0.5, 0.93, 
             summary(precinct), 
             fontname="Times New Roman", 
             ha="center", 
             va="center", 
             fontsize=12)

    pdf.savefig(fig)
    plt.close(fig)

print("Creating PDF")

from matplotlib.backends.backend_pdf import PdfPages 
with PdfPages(filename) as pdf: 
    for prec in precincts["prec_id"]:
        page(prec, pdf)

print("PDF complete")