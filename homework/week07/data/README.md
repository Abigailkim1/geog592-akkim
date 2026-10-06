# Data explanation 

# Analysis 1
## Layer 1: Solar sites and transmission lines 
Data: 
United States Large-Scale Solar Photovoltaic Database from https://www.sciencebase.gov/catalog/item/6671c479d34e84915adb7536 

File names: 
solar_facility_polygons.geojson (vector - polygon)
solar_facility_attributes.csv (attribute)
transmission_lines.geojson (vector - line)

Description: 
I will join the solar facility attribute data to the polygons. I will buffer the solar facility polygons and see how many transmission lines intersect with them. 

Techniques: buffer, intersect 
*Attribute join* 

## Layer 2: 

# Analysis 2
## Layer 3: Smog analysis 
Data: 
Ozone and PM non-attainment areas from https://www.epa.gov/green-book/green-book-8-hour-ozone-2015-area-information

File names: 
ozone_8hr.geojson (vector - polygon)
pm10.geojson (vector - polygon)
pm25.geojson (vector - polygon)

Description: 
I will merge PM10 and PM2.5 non-attainment areas, and then intersect ozone and PM non-attainment areas to look at places at risk for smog. I will calculate the area of each overlap. 

Techniques: merge, intersect 
*Meaningful tabular result*