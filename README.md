# Data-collection-pipeline-arsenal
This script can be used to scrape information on the Arsenal football squad. It can collect data on the men's, women's and men's academy squads, which are the three categories currently available on the website.


The script can be customised to only scrape data on a selection of the categories. This can be done by changing the arguments in the final function call. For example, to just scrape data on the men and women's team, the final line should be "which_to_scrape("men","women")".

All data is put into the "data_folder" folder.

## Unit testing
This repository also include a unit testing script which tests eachs of the methods and functions in 'arsenal_scraper.py'