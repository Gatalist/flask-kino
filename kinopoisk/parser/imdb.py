from bs4 import BeautifulSoup as bs
import re
from .browser import BrowserPlaywright
from tools.loguru_logger import logger


class IMDBMovie(BrowserPlaywright):
    """Получаем кадры с фильма на сайте IMDB с помощью Playwright (синхронная версия)."""

    def __init__(self):
        super().__init__()
        self.base_imdb_url = "https://m.imdb.com/"
        self.film_imdb_url = f"{self.base_imdb_url}title/"
        self.pattern = re.compile(r'https://.*?\.jpg')

    @staticmethod
    def new_base_response_dict():
        """Создаем новый словарь с которого будем формировать ответ сервера"""
        return {
            "status_code": 0,
            "status": False,
            "status_message": '',
            "data": None,
        }

    def check_request_status(self, code):
        """Формируем новый словарь статус с полученными данными"""
        print(f"status_code = {code}\n")
        response = self.new_base_response_dict()

        if code == 200:
            response["status"] = True

        response["status_code"] = code
        # response["status_message"] = Settings.status_codes.get(code, "Error not info")
        return response

    def request_data(self, page: object, url: str):
        """Получаем данные с ответа сервера"""

        response = self.open_url(page=page, link=url, wait_until='domcontentloaded')
        status_code = response.status if response else 400
        new_response = self.check_request_status(status_code)
        if status_code == 200:
            js_code_string = self._extract_image_urls()
            image_urls = page.evaluate(js_code_string)
            new_response["data"] = image_urls

        return new_response

    @staticmethod
    def _extract_image_urls() -> list:
        """
        Функция, выполняемая в контексте браузера, для извлечения
        и фильтрации URL-адресов изображений с помощью JavaScript.
        """
        js_code = """
                () => {
                    const section = document.querySelector('section[data-testid="sub-section-images"]');

                    if (!section) {
                        return [];
                    }

                    const aTags = section.querySelectorAll('a');
                    const screenshotUrls = [];

                    aTags.forEach(a => {
                        const img = a.querySelector('img');

                        if (img && a.hasAttribute('height') && a.hasAttribute('width')) {
                            const height = parseInt(a.getAttribute('height'));
                            const width = parseInt(a.getAttribute('width'));
                            const coef = height / width;

                            if (height < width && coef < 0.8) {
                                screenshotUrls.push(img.src);
                            }
                        }
                    });

                    return [...new Set(screenshotUrls)].slice(0, 12);
                }
            """
        return js_code

    def get_movie_photos(self, imdb_id: str) -> dict:
        """
        Получает скриншоты фильма с IMDB, используя Playwright.

        Args:
            imdb_id: 'tt0290334' (ID фильма на IMDB).

        """
        print('\n----------- IMDB parsing ----------')
        page = self.create_page()
        parse_url = f"{self.film_imdb_url}{imdb_id}/mediaindex/"
        return self.request_data(page=page, url=parse_url)


# old version via requests
# class IMDBMovie(WebRequester):
#     """Получаем кадры с фильма на сайте IMDB"""
#
#     def __init__(self):
#         super().__init__()
#         self.base_imdb_url = "https://m.imdb.com/"
#         self.film_imdb_url = f"{self.base_imdb_url}title/"
#         self.pattern = re.compile(r'https://.*?\.jpg')
#
#     def get_movie_photos(self, imdb_id) -> dict:
#         logger.info(f'\n----------- IMDB parsing ----------')
#         header = self.get_user_agent()
#
#         parse_url = f"{self.film_imdb_url}{imdb_id}/mediaindex/?ref_=mv?ref_=mv_sm"
#         response_data = self.request_data(parse_url, header)
#
#         if response_data["data"]:
#             screenshot = []
#
#             soup = bs(response_data["data"].text, 'html.parser')
#             section = soup.find('section', {'data-testid': 'sub-section-images'})
#             if section:
#                 inner_div = section.find('div')
#                 if inner_div:
#                     a_tags = inner_div.find_all('a')
#                     for a in a_tags:
#                         img = a.find('img')
#                         height = int(a.get('height'))
#                         width = int(a.get('width'))
#                         _coef = height / width
#                         if height < width and _coef < 0.8:
#                             screenshot.append(img.get('src'))
#
#             _images = list(set(screenshot))
#             response_data["data"] = _images[:12]
#         else:
#             response_data["data"] = {}
#
#         return response_data
