# Data explanation 

# Analysis 1
## Layer 1: Solar sites and transmission lines 
Source: 
United States Large-Scale Solar Photovoltaic Database from https://www.sciencebase.gov/catalog/item/6671c479d34e84915adb7536 

File names: 
solar_facility_polygons.geojson (vector - polygon)
solar_facility_attributes.csv (attribute)
transmission_lines.geojson (vector - line)

Description: 
I will join the solar facility attribute data to the polygons. I will buffer the solar facility polygons and see how many transmission lines intersect with them. 

Technique: buffer, intersect 
*Attribute join* 

## Layer 2: 
Source: 
Solar technical potential in Puerto Rico from https://data.nlr.gov/submissions/144 
TIGER/Line Shapefiles from https://www.census.gov/cgi-bin/geo/shapefiles/index.php?year=2007&layergroup=Census+Tracts
Special communities data from https://gis.pr.gov/descargaGeodatos/Delimitaciones/Pages/Comunidades.aspx

File names: 
pr_lmi_solar_potential.csv (attribute)
pr_tracts_2000.geojson (vector - polygon)
special_communities.geojson (vector - polygon)
"This data layer was created by the Geographic Information System Division of the Puerto Rico Department of Housing to locate "Special Communities" (Comunidades Especiales) that receive funding for the construction or rehabilitation of public housing—as well as for other projects—within these communities."

Description: 
I will join the solar potential data to the census tract data. I will then clip that data to the special communities polygons, which are areas that recieve public funding for building or rehabilitation. 

Technique: clip

# Analysis 2
## Layer 3: Smog analysis 
Source: 
Ozone and PM non-attainment areas from https://www.epa.gov/green-book/green-book-8-hour-ozone-2015-area-information

File names: 
ozone_8hr.geojson (vector - polygon)
pm10.geojson (vector - polygon)
pm25.geojson (vector - polygon)

Description: 
I will merge PM10 and PM2.5 non-attainment areas, and then intersect ozone and PM non-attainment areas to look at places at risk for smog. I will calculate the area of each overlap. 

Technique: merge, intersect
*Meaningful tabular result*