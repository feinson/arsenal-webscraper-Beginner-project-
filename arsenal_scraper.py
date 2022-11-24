import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

class ArsenalScraper:
    num_categories = 0
    site = "https://www.arsenal.com/"

    def __init__(self, category):
        '''The function takes in a category as an argument and assigns it to the instance variable category. It
        then creates a url by concatenating the category with the base url. It then increments the class
        variable num_categories by 1. Finally, it checks if the data_folder exists and if it doesn't, it
        creates it.
        
        Parameters
        ----------
        category
            This is the category of the player. It can be either first-team, u23, u18, u23-coaching-staff,
        u18-coaching-staff, first-team-coaching-staff, first-team-medical-staff, first-team-back
        
        '''
        

        self.category = category
        self.url = f"https://www.arsenal.com/{self.category}/players"
        ArsenalScraper.num_categories +=1
        if not os.path.exists("./data_folder"):
            os.mkdir("./data_folder")


    @staticmethod
    def make_soup(url):
        '''It takes a url as an argument, makes a request to that url, and returns a BeautifulSoup object
        
        Parameters
        ----------
        url
            the url of the page you want to scrape
        
        Returns
        -------
            the soup object.
        
        '''
        soup = BeautifulSoup(requests.get(url).content, "html.parser")
        return soup

    def create_photo_directory(self):
        '''It creates a directory in the data_folder directory with the name of the category and the word
        photos
        
        '''
        if not os.path.exists(f"./data_folder/{self.category}_photos"):
            os.mkdir(f"./data_folder/{self.category}_photos")

    
    def save_photo_from_page_soup(self, soup, name):
        img_frame = soup.find("img", class_ = "article-card-header__image")
        img_source = f"{ArsenalScraper.site}{img_frame.get('src')}"
        underscore_name = name.replace(" ", "_")


        file_path = f"./data_folder/{self.category}_photos/{underscore_name}.jpg"



        img_content = requests.get(img_source).content

        with open(file_path, "wb") as f:
            f.write(img_content)
    

    def get_player_links_and_positions(self):
        '''It produces a list of two-long sublists. Each sublist contains the link to a player profile, as 
        well as their position category.
        
        Returns
        -------
            A list of lists. Each list contains the category title and the link to the player's page.
        
        '''
        soup = self.make_soup(self.url)
        player_block = soup.find("div", {"id": "block-arsenal-main-content"})

        position_title_list, output_list = [], []
        position_title_frame_list = player_block.find_all("h2", class_="u-title-line")
        for position_title_frame in position_title_frame_list:
            position_title_list.append(position_title_frame.get_text())

        position_frame_list = player_block.find_all("div", class_="smart-grid")

        for i, position_frame in enumerate(position_frame_list):
            link_frames = position_frame.find_all("a", class_="player-card__wrapper player-card__wrapper--link")

            for link_frame in link_frames:
                rel_link = link_frame.get('href')
                link = f"{ArsenalScraper.site}{rel_link}"
                output_list.append([position_title_list[i], link])

        return output_list


    def get_player_information(self, input_list):
        '''It takes a list of information about a player, and adds to it the player's name, squad number,
        and date of birth. It also downloads the player's photo and saves it in a folder
        
        Parameters
        ----------
        input_list
            a list of the player's name, link, and position
        
        '''
        try:
            soup = ArsenalScraper.make_soup(input_list[1])

            try_table = soup.find("div", class_="responsive-table")
            if try_table != None:
                info_boxes = try_table.find_all("td")
                name, squad_number, born = [info_boxes[i].get_text() for i in range(3)]
                
            else:
                try_table = soup.find("div", class_="card card--padded info-card")
                info_boxes = try_table.find_all("dd", class_="info-card__value")
                name, squad_number = [info_boxes[i].get_text() for i in range(2)]
                born = (info_boxes[2].get_text()).split("/")[0]

            input_list.extend([name, squad_number, born])

            self.save_photo_from_page_soup(soup, name)
        except:
            pass

# Categories: men, academy, women
def scrape_categories(*categories_to_scrape):
    '''It takes in a list of categories, which should be any combination of "men", "women", "academy".
    It creates a folder for each category, in which to store the photos of the players. It then scrapes the squad data for each
    category from the Arsenal website, and saves the tabular data as a csv file, as well as saving the photos to the relevant folder.
    
    '''

    for category in categories_to_scrape:

        scraper = ArsenalScraper(category)

        scraper.create_photo_directory()
        
        lists_of_player_data = scraper.get_player_links_and_positions()

        for j, _ in enumerate(lists_of_player_data):
            scraper.get_player_information(lists_of_player_data[j])

        data = pd.DataFrame(lists_of_player_data)
        data.columns = ["Position", "Link to Profile Page", "Name", "Squad Number", "D.O.B"]

        data.to_csv(f"./data_folder/{category}_squad.csv")

if __name__ == "__main__":
    scrape_categories("women")