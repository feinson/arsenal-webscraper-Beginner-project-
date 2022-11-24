import unittest
import arsenal_scraper
import os
import bs4
import shutil

ArsenalScraper = arsenal_scraper.ArsenalScraper

class TestArsenalScraper(unittest.TestCase):


    def setUp(self) -> None:

        self.men = ArsenalScraper("men")
        self.women = ArsenalScraper("women")
        self.academy = ArsenalScraper("academy")
        self.list_of_instances = [self.men, self.women, self.academy]

    def test_make_soup(self):

        for instance in self.list_of_instances:

            soup = ArsenalScraper.make_soup(instance.url)
            self.assertTrue(isinstance(soup, bs4.BeautifulSoup))

    def test_create_photo_directory(self):

        for instance in self.list_of_instances:

            instance.create_photo_directory()
            self.assertTrue(os.path.exists(f"./data_folder/{instance.category}_photos"))
            os.rmdir(f"./data_folder/{instance.category}_photos")

    def test_save_photo(self):

        test_url = "https://www.arsenal.com/men/players/emile-smith-rowe"

        for instance in self.list_of_instances:
            instance.create_photo_directory()
            soup = ArsenalScraper.make_soup(test_url)
            instance.save_photo_from_page_soup(soup, "Emile Smith Rowe")
            self.assertTrue(os.path.exists(f"./data_folder/{instance.category}_photos/Emile_Smith_Rowe.jpg"))
            shutil.rmtree(f"./data_folder/{instance.category}_photos")

    def test_get_player_links(self):

        for instance in self.list_of_instances:
            list_of_player_links_and_positions = instance.get_player_links_and_positions()

        self.assertEqual(len(list_of_player_links_and_positions[0]),2)
        self.assertIsInstance(list_of_player_links_and_positions, list)

    def test_get_player_information(self):
        for instance in self.list_of_instances:
            test_input = ["Goalkeepers", "https://www.arsenal.com/men/players/emile-smith-rowe"]
            instance.create_photo_directory()
            instance.get_player_information(test_input)
            self.assertEqual(len(test_input),5)
            self.assertIsInstance(test_input,list)
            shutil.rmtree(f"./data_folder/{instance.category}_photos")

    def test_scrape_categories(self):
        arsenal_scraper.scrape_categories("men", "women", "academy")
        for category in ["men", "women", "academy"]:
            self.assertTrue(os.path.exists(f"./data_folder/{category}_squad.csv"))
            os.remove(f"./data_folder/{category}_squad.csv")
            shutil.rmtree(f"./data_folder/{category}_photos")
    

if __name__ == "__main__":
    unittest.main()