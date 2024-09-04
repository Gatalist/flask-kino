from bs4 import BeautifulSoup as bs
import re
from settings import Settings
from .base_parser import WebRequester


class WebRequesterMovieScreenshotIMDB(WebRequester):
    """Получаем кадры с фильма на сайте IMDB"""

    def __init__(self):
        self.film_imdb_url = f"{Settings.base_imdb_url}title/"
        self.pattern = re.compile(r'https://.*?\.jpg')

    def request_screenshot(self, imdb_id) -> dict:
        print(f'\n----------- IMDB parsing ----------')
        header = self.get_user_agent()

        parse_url = f"{self.film_imdb_url}{imdb_id}"
        screenshot_request_data = self.request_data(parse_url, header)

        if screenshot_request_data["data"]:
            screenshot = []

            soup = bs(screenshot_request_data["data"].text, 'html.parser')
            find_class = "ipc-shoveler ipc-shoveler--base ipc-shoveler--page0"
            div_tags = soup.find('div', class_=find_class)

            if div_tags:
                for img_tag in div_tags.find_all('img', class_='ipc-image'):
                    img_url = img_tag.get('srcset')
                    if img_url:
                        matches = self.pattern.findall(img_url)
                        screenshot.append(matches[-1])

            #  возвращаем картинки
            screenshot_request_data["data"] = list(set(screenshot))
            return screenshot_request_data

        screenshot_request_data["data"] = {}
        return screenshot_request_data
