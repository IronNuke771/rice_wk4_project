"""
Project for Week 3 of "Python Data Visualization".
Unify data via common country name.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""

import csv
import math
import pygal

def read_csv_as_nested_dict(filename, keyfield, separator, quote):
    """
    Inputs:
      filename  - Name of CSV file
      keyfield  - Field to use as key for rows
      separator - Character that separates fields
      quote     - Character used to optionally quote fields

    Output:
      Returns a dictionary of dictionaries where the outer dictionary
      maps the value in the key_field to the corresponding row in the
      CSV file.  The inner dictionaries map the field names to the
      field values for that row.
    """
    return_dict = {}
    with open(filename, newline='') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=separator, quotechar=quote)
        for row in csvreader:
            row_key = row[keyfield]
            return_dict[row_key] = row
    return return_dict

def reconcile_countries_by_name(plot_countries, gdp_countries):
    """
    Inputs:
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      gdp_countries  - Dictionary whose keys are country names used in GDP data

    Output:
      A tuple containing a dictionary and a set.  The dictionary maps
      country codes from plot_countries to country names from
      gdp_countries The set contains the country codes from
      plot_countries that were not found in gdp_countries.
    """
    recon_dict = {}
    recon_set = set()
    for c_code,c_name in plot_countries.items():
        if c_name in gdp_countries:
            recon_dict[c_code] = c_name
        else:
##            print(c_code,c_name)
            recon_set.add(c_code)
##    for key,val in recon_dict.items():
##        print(key,val)
##    print("")
##    print(recon_set)
##    print("")
##    print(len(recon_dict),len(recon_set))
    
    return recon_dict, recon_set


def build_map_dict_by_name(gdpinfo, plot_countries, year):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      year           - String year to create GDP mapping for

    Output:
      A tuple containing a dictionary and two sets.  The dictionary
      maps country codes from plot_countries to the log (base 10) of
      the GDP value for that country in the specified year.  The first
      set contains the country codes from plot_countries that were not
      found in the GDP data file.  The second set contains the country
      codes from plot_countries that were found in the GDP data file, but
      have no GDP data for the specified year.
    """
    gdp_year_dict = read_csv_as_nested_dict(gdpinfo["gdpfile"],
                                       gdpinfo["country_name"],
                                       gdpinfo["separator"],
                                       gdpinfo["quote"])
    pygal_gdp_dict = {}
    set_one = set()
    set_two = set()
    for ccode,cname in plot_countries.items():
        if cname in gdp_year_dict:
##            print(ccode,gdp_year_dict[cname][year])
            ann_gdp = gdp_year_dict[cname][year]
            if ann_gdp.isnumeric and len(ann_gdp):
                log_ann_gdp = math.log(float(ann_gdp),10)
                pygal_gdp_dict[ccode] = log_ann_gdp
            else:
                # this will be the 2nd set
                set_two.add(ccode)
        else:
            # this will be the 1st set
            set_one.add(ccode)
##    print(pygal_gdp_dict)
##    print("set 1: ",set_one)
##    print("set 2: ",set_two)

    return pygal_gdp_dict, set_one, set_two


def render_world_map(gdpinfo, plot_countries, year, map_file):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      year           - String year to create GDP mapping for
      map_file       - Name of output file to create

    Output:
      Returns None.

    Action:
      Creates a world map plot of the GDP data for the given year and
      writes it to a file named by map_file.
    """
    gdpinfo = {
        "gdpfile": "isp_gdp.csv",
        "separator": ",",
        "quote": '"',
        "min_year": 1960,
        "max_year": 2015,
        "country_name": "Country Name",
        "country_code": "Country Code"
        }
    gdp_dict = read_csv_as_nested_dict(gdpinfo["gdpfile"],
                                       gdpinfo["country_name"],
                                       gdpinfo["separator"],
                                       gdpinfo["quote"])
    pygal_countries = pygal.maps.world.COUNTRIES
    plot_countries = reconcile_countries_by_name(pygal_countries, gdp_dict)
    map_data = build_map_dict_by_name(gdpinfo, plot_countries[0], year)
    
    # Build the map
    worldmap_chart = pygal.maps.world.World()
    worldmap_chart.title = 'Global GDP by Country for ' + str(year)
    worldmap_chart.add("GDP",map_data[0])
    worldmap_chart.add("Not in WB Data",map_data[1])
    worldmap_chart.add("no GDP data",map_data[2])
    worldmap_chart.render_in_browser()

    
    return


def test_render_world_map():
    """
    Test the project code for several years.
    """
    gdpinfo = {
        "gdpfile": "isp_gdp.csv",
        "separator": ",",
        "quote": '"',
        "min_year": 1960,
        "max_year": 2015,
        "country_name": "Country Name",
        "country_code": "Country Code"
    }

    # Get pygal country code map
    pygal_countries = pygal.maps.world.COUNTRIES

    # 1960
    render_world_map(gdpinfo, pygal_countries, "1960", "isp_gdp_world_name_1960.svg")

    # 1980
    render_world_map(gdpinfo, pygal_countries, "1980", "isp_gdp_world_name_1980.svg")

    # 2000
    render_world_map(gdpinfo, pygal_countries, "2000", "isp_gdp_world_name_2000.svg")

    # 2010
    render_world_map(gdpinfo, pygal_countries, "2010", "isp_gdp_world_name_2010.svg")


# Make sure the following call to test_render_world_map is commented
# out when submitting to OwlTest/CourseraTest.

##test_render_world_map()
########################################################################
##
##gdpinfo = {
##    "gdpfile": "isp_gdp.csv",
##    "separator": ",",
##    "quote": '"',
##    "min_year": 1960,
##    "max_year": 2015,
##    "country_name": "Country Name",
##    "country_code": "Country Code"
##    }
##gdp_dict = read_csv_as_nested_dict(gdpinfo["gdpfile"],
##                                       gdpinfo["country_name"],
##                                       gdpinfo["separator"],
##                                       gdpinfo["quote"])
##pygal_countries = pygal.maps.world.COUNTRIES
### problem 1 call   
##plot_countries = reconcile_countries_by_name(pygal_countries, gdp_dict)
### problem 2 call
##build_map_dict_by_name(gdpinfo, plot_countries[0], "2000")
### problem 4 call
##render_world_map(gdpinfo, pygal_countries, "2000", "test_world.csv")

