import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

class ArsenalScraper:
    num_categories = 0
    site = "https://www.arsenal.com/"

    def __init__(self, category):

        self.category = category
        self.response = requests.get(f"https://www.arsenal.com/{self.category}/players")
        ArsenalScraper.num_categories +=1
    

    def get_player_links(self):
        soup = BeautifulSoup(self.response.content, "html.parser")
        player_block = soup.find("div", {"id": "block-arsenal-main-content"})

        category_title_list, output_list = [], []
        category_title_frame_list = player_block.find_all("h2", class_="u-title-line")
        for category_title_frame in category_title_frame_list:
            category_title_list.append(category_title_frame.get_text())

        category_frame_list = player_block.find_all("div", class_="smart-grid")

        for i, category_frame in enumerate(category_frame_list):
            link_frames = category_frame.find_all("a", class_="player-card__wrapper player-card__wrapper--link")

            for link_frame in link_frames:
                rel_link = link_frame.get('href')
                link = f"{ArsenalScraper.site}{rel_link}"
                output_list.append([category_title_list[i], link])

        return output_list

    def link_to_information(self, input_list):
        try:
            sub_response = requests.get(input_list[1])
            soup = BeautifulSoup(sub_response.content, "html.parser")


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

            img_frame = soup.find("img", class_ = "article-card-header__image")
            img_source = f"{ArsenalScraper.site}{img_frame.get('src')}"

            underscore_name = name.replace(" ", "_")
            img_content = requests.get(img_source).content
            file_path = f"./data_folder/{self.category}_photos/{underscore_name}.jpg"

            with open(file_path, "wb") as f:
                f.write(img_content)
        except:
            pass


# Categories: men, academy, women
def which_to_scrape(*categories_to_scrape):

    for category in categories_to_scrape:

        os.mkdir(f"./data_folder/{category}_photos")

        scraper = ArsenalScraper(category)
        listy = scraper.get_player_links()

        for j, player in enumerate(listy):
            scraper.link_to_information(listy[j])

        data = pd.DataFrame(listy)
        data.columns = ["Category", "Link to Profile Page", "Name", "Squad Number", "D.O.B"]
        data.to_csv(f"./data_folder/{category}_squad.csv")

which_to_scrape("men","academy")