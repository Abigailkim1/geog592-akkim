# Data explanation 

## Large scale solar facilities in the US 
United States Large-Scale Solar Photovoltaic Database from https://www.sciencebase.gov/catalog/item/6671c479d34e84915adb7536 

My data folder contains a geojson named "solar_facility_polygons", which contains vector data outlining each solar facility. The file "solar_facility_attributes" is a csv with attribute data. I will join the the attribute data to the vector data and filter for North Carolina. I will buffer the solar polygons and see how many transmisison lines intersect with them. 

Ozone non-attainment areas https://www.epa.gov/green-book/green-book-8-hour-ozone-2015-area-information
Intersect with PM non-attainment areas to look at places at risk for smog. 
Technique: spatial join, intersect 
Find the area for each and add to the table.   

Puerto Rico Solar-for-All: LMI PV Rooftop Technical Potential and Solar Savings Potential https://www.osti.gov/dataexplorer/biblio/dataset/1676962

Join to census tract data in pr_tracts.geojson