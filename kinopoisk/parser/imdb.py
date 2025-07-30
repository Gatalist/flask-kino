from bs4 import BeautifulSoup as bs
import re
from .base_parser import WebRequester
from tools.loguru_logger import logger


class IMDBMovie(WebRequester):
    """Получаем кадры с фильма на сайте IMDB"""

    def __init__(self):
        super().__init__()
        self.base_imdb_url = "https://m.imdb.com/"
        self.film_imdb_url = f"{self.base_imdb_url}title/"
        self.pattern = re.compile(r'https://.*?\.jpg')

    def get_movie_photos(self, imdb_id) -> dict:
        logger.info(f'\n----------- IMDB parsing ----------')
        header = self.get_user_agent()

        parse_url = f"{self.film_imdb_url}{imdb_id}/mediaindex/?ref_=mv?ref_=mv_sm"
        response_data = self.request_data(parse_url, header)

        if response_data["data"]:
            screenshot = []

            soup = bs(response_data["data"].text, 'html.parser')
            section = soup.find('section', {'data-testid': 'sub-section-images'})
            if section:
                inner_div = section.find('div')
                if inner_div:
                    a_tags = inner_div.find_all('a')
                    for a in a_tags:
                        img = a.find('img')
                        height = int(a.get('height'))
                        width = int(a.get('width'))
                        _coef = height / width
                        if height < width and _coef < 0.8:
                            screenshot.append(img.get('src'))

            _images = list(set(screenshot))
            response_data["data"] = _images[:12]
        else:
            response_data["data"] = {}

        return response_data
