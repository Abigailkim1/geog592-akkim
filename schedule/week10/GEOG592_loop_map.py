import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt


# In[8]:


# getting the US census data

url_0 = "https://www2.census.gov/geo/tiger/GENZ2024/shp/" # url for census tiger data 
url_county = "cb_2024_us_county_500k.zip" # county level
url_state = "cb_2024_us_state_500k.zip" # state level 


## Code for county level data 

counties = gpd.read_file(url_0+url_county)
nc_counties = counties.loc[counties["STATEFP"] == "37"].to_crs(6543).copy()
nc_counties.plot(edgecolor="black", facecolor="white")


# In[9]:


# Map only Durham 
durham = nc_counties[nc_counties["NAME"] == "Durham"]

durham.plot(edgecolor="black", facecolor="white")


# In[ ]:





# In[11]:


#Let's make a locator map
ax = nc_counties.plot(edgecolor="gray", facecolor="white")

durham.plot(ax=ax, edgecolor="black", facecolor="#7b9b90")

ax.set_axis_off()


# In[12]:


#let's make each into a function with county and ax being the parameter

def county_map(county, ax):
    selected = nc_counties[nc_counties["NAME"] == county]
    selected.plot(ax=ax, edgecolor="black", facecolor="#7b9b90")
    ax.set_axis_off()


def locator_map(county, ax):
    selected = nc_counties[nc_counties["NAME"] == county]
    nc_counties.plot(ax=ax, edgecolor="gray", facecolor="white")
    selected.plot(ax=ax, edgecolor="black", facecolor="#7b9b90")
    ax.set_axis_off()


# In[13]:


#Let's test putting them in the same figure
fig, axes = plt.subplots(1, 2, figsize=(12, 6))

county_map("Durham", axes[0])
locator_map("Durham", axes[1])

plt.show()


# In[14]:


fig, axes = plt.subplots(
    1, 2,
    figsize=(12, 6),
    gridspec_kw={"width_ratios": [3, 1]}
)

county_map("Durham", axes[0])
locator_map("Durham", axes[1])

# If you use the geopandas .plot() method, it automatically shows and you don't need this line.
plt.show()


# In[15]:


fig, axes = plt.subplots(
    2, 1,
    figsize=(8, 10),
    gridspec_kw={"height_ratios": [3, 1]}
)

county_map("Durham", axes[0])
locator_map("Durham", axes[1])


# In[16]:


fig, axes = plt.subplots(
    2, 1,
    figsize=(8, 10),
    gridspec_kw={"height_ratios": [3, 1]}
)

county_map("Durham", axes[0])
locator_map("Durham", axes[1])
fig.suptitle("Durham County", fontsize=20)


# In[17]:


# Let's make this a funtions too and add the fig.save into a pdf
def county_figure(county):
    fig, axes = plt.subplots(
        2, 1,
        figsize=(8, 10),
        gridspec_kw={"height_ratios": [3, 1]}
    )

    county_map(county, axes[0])
    locator_map(county, axes[1])

    fig.suptitle(f"{county} County", fontsize=20)

    fig.savefig(f"{county}_County.pdf")
    plt.close(fig)


# In[18]:


county_figure("Durham")


# In[19]:


## Let's make a function that will put all the pdfs into one PDF

def county_figure(county, pdf):
    fig, axes = plt.subplots(
        2, 1,
        figsize=(8, 10),
        gridspec_kw={"height_ratios": [3, 1]}
    )

    county_map(county, axes[0])
    locator_map(county, axes[1])

    fig.suptitle(f"{county} County", fontsize=20)

    pdf.savefig(fig)
    plt.close(fig)


# In[20]:


from matplotlib.backends.backend_pdf import PdfPages 
# we will use this module to save the pdfs into a file


# In[21]:


# This might take a few seconds
with PdfPages("NC_Counties.pdf") as pdf:  #with #manages a resource and automatically cleans up when you finish using it.
    for county in nc_counties["NAME"]:
        county_figure(county, pdf)


# In[ ]:


#Let's make the pages a bit more interesting 
fig, axes = plt.subplots(
    2, 2,
    figsize=(12, 10),
    gridspec_kw={
        "height_ratios": [3, 1],
        "width_ratios": [2, 1]
    }
)

county_map("Durham", axes[0, 0])
locator_map("Durham", axes[1, 0])

axes[0, 1].set_title("Land and water pie chart")
axes[1, 1].set_title("Land and water information")

for ax in axes.flat:
    ax.set_axis_off()


# In[23]:


# Making a pie chart function
def county_pie(county, ax):
    selected = nc_counties[nc_counties["NAME"] == county]

    land = selected["ALAND"].iloc[0]
    water = selected["AWATER"].iloc[0]

    ax.pie(
        [land, water],
        labels=["Land", "Water"],
        colors=["olivedrab", "steelblue"],
        autopct="%.1f%%",
        startangle=90
    )

    ax.set_title("Land and water")


# In[24]:


#Let's make out pages a bit more interesting 
fig, axes = plt.subplots(
    2, 2,
    figsize=(12, 10),
    gridspec_kw={
        "height_ratios": [3, 1],
        "width_ratios": [2, 1]
    }
)

county_map("Durham", axes[0, 0])
locator_map("Durham", axes[1, 0])
county_pie("Durham", axes[0,1])
# axes[0, 1].set_title("Land and water pie chart")
axes[1, 1].set_title("Land and water information")

for ax in axes.flat:
    ax.set_axis_off()

fig.suptitle("Durham", fontsize=30)


# In[25]:


def county_info(county, ax):
    selected = nc_counties[nc_counties["NAME"] == county]

    land = selected["ALAND"].iloc[0]
    water = selected["AWATER"].iloc[0]

    land_km2 = land / 1_000_000
    water_km2 = water / 1_000_000

    land_mi2 = land / 2_589_988.110336
    water_mi2 = water / 2_589_988.110336

    ax.text(
        0.1, 0.8,
        f"LAND\n{land_km2:,.2f} km²\n{land_mi2:,.2f} square miles",
        transform=ax.transAxes,
        fontsize=14,
        color="olivedrab",
        va="top"
    )

    ax.text(
        0.1, 0.4,
        f"WATER\n{water_km2:,.2f} km²\n{water_mi2:,.2f} square miles",
        transform=ax.transAxes,
        fontsize=14,
        color="steelblue",
        va="top"
    )

    ax.set_axis_off()


# In[26]:


#Let's make out pages a bit more interesting 
fig, axes = plt.subplots(
    2, 2,
    figsize=(12, 10),
    gridspec_kw={
        "height_ratios": [3, 1],
        "width_ratios": [2, 1]
    }
)

county_map("Durham", axes[0, 0])
locator_map("Durham", axes[1, 0])
county_pie("Durham", axes[1,1])
county_info("Durham",  axes[0,1])
# axes[0, 1].set_title("Land and water pie chart")
# axes[1, 1].set_title("Land and water information")

for ax in axes.flat:
    ax.set_axis_off()

fig.suptitle("Durham", fontsize=30)


# In[27]:


from matplotlib.patches import Polygon, Ellipse

def county_info(county, ax):
    selected = nc_counties[nc_counties["NAME"] == county]

    land = selected["ALAND"].iloc[0]
    water = selected["AWATER"].iloc[0]

    ## Using ai and https://matplotlib.org/stable/gallery/shapes_and_collections/hatch_demo.html
    # Land icon: mountains
    mountain = Polygon(
        [(0.02, 0.60), (0.09, 0.80), (0.14, 0.69),
         (0.19, 0.76), (0.25, 0.60)],
        facecolor="olivedrab",
        transform=ax.transAxes
    )
    ax.add_patch(mountain)

    # Water icon
    lake = Ellipse(
        (0.13, 0.30),
        width=0.23,
        height=0.12,
        facecolor="steelblue",
        transform=ax.transAxes
    )
    ax.add_patch(lake)

    ax.text(
        0.32, 0.80,
        f"LAND\n{land / 1_000_000:,.2f} km²\n"
        f"{land / 2_589_988.110336:,.2f} square miles",
        transform=ax.transAxes,
        fontsize=14,
        color="olivedrab",
        va="top"
    )

    ax.text(
        0.32, 0.40,
        f"WATER\n{water / 1_000_000:,.2f} km²\n"
        f"{water / 2_589_988.110336:,.2f} square miles",
        transform=ax.transAxes,
        fontsize=14,
        color="steelblue",
        va="top"
    )

    ax.set_axis_off()


# In[28]:


fig, axes = plt.subplots(
    2, 2,
    figsize=(12, 10),
    gridspec_kw={
        "height_ratios": [3, 1],
        "width_ratios": [2, 1]
    }
)

county_map("Durham", axes[0, 0])
locator_map("Durham", axes[1, 0])
county_pie("Durham", axes[1,1])
county_info("Durham",  axes[0,1])
# axes[0, 1].set_title("Land and water pie chart")
# axes[1, 1].set_title("Land and water information")

for ax in axes.flat:
    ax.set_axis_off()

fig.suptitle("Durham", fontsize=30)


# In[29]:


#Let's make it nicer 

county = "Durham"

fig = plt.figure(figsize=(12, 8))

# [left, bottom, width, height] as fractions of the figure
# Coded with Ai help
ax_county = fig.add_axes([0.05, 0.23, 0.55, 0.54])
ax_locator = fig.add_axes([0.05, 0.08, 0.25, 0.12])
ax_pie = fig.add_axes([0.65, 0.48, 0.30, 0.30])
ax_info = fig.add_axes([0.65, 0.12, 0.30, 0.32])


county_map(county, ax_county)
locator_map(county, ax_locator)
county_pie(county, ax_pie)
county_info(county, ax_info)

# Page heading
fig.text(
    0.05, 0.94,
    "NORTH CAROLINA / County Water-Land Atlas",
    fontsize=10,
    color="olivedrab"
)

fig.text(
    0.05, 0.87,
    f"{county} County",
    fontsize=28,
    fontweight="bold"
)

# Footer
fig.text(
    0.05, 0.03,
    "Source: U.S. Census Bureau | Areas from ALAND and AWATER",
    fontsize=9,
    color="gray"
)

plt.show()


# In[30]:


#Let's make it a function

def county_figure(county, pdf):

    fig = plt.figure(figsize=(12, 8))

    # [left, bottom, width, height] as fractions of the figure
    # Coded with Ai help
    ax_county = fig.add_axes([0.05, 0.23, 0.55, 0.54])
    ax_locator = fig.add_axes([0.05, 0.08, 0.25, 0.12])
    ax_pie = fig.add_axes([0.65, 0.48, 0.30, 0.30])
    ax_info = fig.add_axes([0.65, 0.12, 0.30, 0.32])


    county_map(county, ax_county)
    locator_map(county, ax_locator)
    county_pie(county, ax_pie)
    county_info(county, ax_info)

    # Page heading
    fig.text(
        0.05, 0.94,
        "NORTH CAROLINA / County Water-Land Atlas",
        fontsize=10,
        color="olivedrab"
    )

    fig.text(
        0.05, 0.87,
        f"{county} County",
        fontsize=28,
        fontweight="bold"
    )

    # Footer
    fig.text(
        0.05, 0.03,
        "Source: U.S. Census Bureau | Areas from ALAND and AWATER",
        fontsize=9,
        color="gray"
    )

    pdf.savefig(fig, dpi=50)
    plt.close(fig)


# In[31]:


# This might take a few seconds and you need at least 40MB of free space in your computer
with PdfPages("NC_Counties.pdf") as pdf:  #with #manages a resource and automatically cleans up when you finish using it.
    for county in nc_counties["NAME"]:
        county_figure(county, pdf)


# In[32]:


# It would look nicer if it is in Alphabetical Order.
nc_counties = nc_counties.sort_values("NAME").reset_index(drop=True)
# This might take a few seconds and you need at least 40MB of free space in your computer
with PdfPages("NC_Counties.pdf") as pdf:  #with #manages a resource and automatically cleans up when you finish using it.
    for county in nc_counties["NAME"]:
        county_figure(county, pdf)


# In[33]:


# other information in case someone wants to add a scale but currently it does not work well with certain counties
# ax.add_artist(
#     ScaleBar(
#         dx=1,              
#         units="ft",
#         dimension="imperial-length",
#         location="lower right",
#         fixed_value= 5,
#         fixed_units="mi",
#         length_fraction=1,
#         box_alpha=0
#     )
# )

