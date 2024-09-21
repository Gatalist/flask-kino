from bs4 import BeautifulSoup as bs
import re
from .parser import WebRequester


class WebRequesterIMDB(WebRequester):
    """Получаем кадры с фильма на сайте IMDB"""

    def __init__(self):
        self.base_imdb_url = "https://m.imdb.com"
        self.film_imdb_url = f"{self.base_imdb_url}/title/"
        self.pattern = re.compile(r'https://.*?\.jpg')

    def request_screenshot(self, imdb_id) -> dict:
        print(f'\n----------- IMDB parsing ----------')
        headers = self.get_user_agent()

        parse_url = f"{self.film_imdb_url}{imdb_id}"
        screenshot_request_data = self.request_data(url=parse_url, headers=headers, response_type='text')

        if screenshot_request_data.get("result"):
            screenshot = []

            soup = bs(screenshot_request_data["result"], 'html.parser')
            find_class = "ipc-shoveler ipc-shoveler--base ipc-shoveler--page0"
            div_tags = soup.find('div', class_=find_class)

            if div_tags:
                for img_tag in div_tags.find_all('img', class_='ipc-image'):
                    img_url = img_tag.get('srcset')
                    if img_url:
                        matches = self.pattern.findall(img_url)
                        screenshot.append(matches[-1])

            #  возвращаем картинки
            screenshot_request_data["result"] = list(set(screenshot))
            return screenshot_request_data

        screenshot_request_data["result"] = {}
        return screenshot_request_data
