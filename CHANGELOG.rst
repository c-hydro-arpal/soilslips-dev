=========
Changelog
=========

Version 2.5.0 [2024-10-10]
**************************
- PROJECT: Operational release
- TOOL: arpal_soil_slips_scenarios_main.py
	- Fix bugs in time selection (rain and soil moisture variables) 
	- Fix bugs in computing indicators (rain and soil moisture variables)
	- Add left and right selection period (rain and soil moisture variables)

Version 2.4.0 [2024-07-10]
**************************
- PROJECT: Operational release
- TOOL: arpal_soil_slips_scenarios_main.py
	- Fix bugs in regridding rain maps (pyresample algorithm)
	- Fix bugs in read ascii grid data (error of epsg code not available in the coordinates system db)
	- Add GDAL_DATA in mandatory algorithm dependencies

Version 2.3.0 [2024-01-16]
**************************
- PROJECT: Operational release
- TOOL: arpal_soil_slips_viewer_main.py


Version 2.2.0 [2023-01-18]
**************************
- PROJECT: Operational release
- APP: arpal_soil_slips_scenarios_main.py
	- Add support to xls and xlsx weather stations file
	- Add automatic detection of soil-slips alert area

Version 2.1.2 [2022-10-13]
**************************
- PROJECT: Operational release
- APP: arpal_soil_slips_predictors_main.py
	- Fix bugs to the kernel fx
	
Version 2.1.1 [2022-04-13]
**************************
- PROJECT: Operational release
- APP: arpal_soil_slips_scenarios_main.py
	- Fix bugs and refactor methods
- APP: arpal_soil_slips_predictors_main.py
	- Fix bugs and refactor methods

Version 2.1.0 [2022-03-20]
**************************
- PROJECT: Pre-operational release

Version 2.0.0 [2022-04-13]
**************************
- PROJECT: Pre-operational release
- APP: arpal_soil_slips_scenarios_main.py
- APP: arpal_soil_slips_predictors_main.py

Version 1.4.1 [2022-01-05]
**************************
- PROJECT: Pre-operational release
- APP: Jupyter Notebook for analyzing soilslips series

Version 1.4.0 [2021-05-15]
**************************
- PROJECT: beta release
- APP: arpal_soil_slips_scenarios_main.py
	- Add rain maps limits checks
	- Add unique scenarios .csv file
	- Fix rain peaks computations

Version 1.3.0 [2021-04-12]
**************************
- PROJECT: beta release
- APP: arpal_soil_slips_scenarios_main.py
	- Add dependencies management
	- Add forcing point creation for saving rain peaks

Version 1.2.1 [2021-03-19]
**************************
- PROJECT: beta release
- APP: arpal_soil_slips_scenarios_main.py
	- Fix bugs in creating output indicators files
	- Fix bugs in creating scenarios csv and png files

Version 1.2.0 [2021-02-02]
**************************
- PROJECT: beta release
- APP: arpal_soil_slips_scenarios_main.py
	- Fix bugs in creating rain datasets
	- Fix bugs in output csv scenarios files

Version 1.1.0 [2020-11-25]
**************************
- PROJECT: beta release
- APP: arpal_soil_slips_scenarios_main.py
	- Update reader and writer methods for rain variable
	- Update reader and writer methods for soil moisture variables

Version 1.0.0 [2020-05-15]
**************************
- PROJECT: beta release
- APP: arpal_soil_slips_scenarios_main.py
	
Version 0.0.1 [2020-05-10]
**************************
- PROJECT: first commit to open the repository and initialize the default settings


