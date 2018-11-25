from bs4 import BeautifulSoup
import requests


class KinopoiskParser:
    def __init__(self, user_id, current_page=1):
        self._user_id = user_id
        self._current_page = current_page
        self._wasted_time_in_minutes = 0

    def calculate_wasted_time(self, proxy_manager):
        while True:
            film_list_url = f'https://www.kinopoisk.ru/user/{self._user_id}' \
                f'/votes/list/ord/date/genre/films/page/{self._current_page}/#list'

            try:
                film_response = requests.get(film_list_url, proxies=proxy_manager.get_proxies()).text
            except BaseException:
                proxy_manager.update_proxy()
                continue

            user_page = BeautifulSoup(film_response, "html.parser")

            is_captcha = self._check_that_is_captcha(user_page)
            if is_captcha:
                proxy_manager.update_proxy()
                continue

            is_end = self._check_that_is_end_of_film_list(user_page)
            if is_end:
                break

            wasted_time = self._get_film_duration_on_page(user_page)
            self._wasted_time_in_minutes += wasted_time

            print(f'Page {self._current_page}, wasted time {self._wasted_time_in_minutes}')

            self._move_next_page()

    def get_wasted_time(self):
        return self._wasted_time_in_minutes

    def _move_next_page(self):
        self._current_page += 1

    @staticmethod
    def _get_film_duration_on_page(user_page):
        try:
            wasted_time = 0
            film_list = user_page.findAll("div", {"class": "profileFilmsList"})[0].findAll("div", {"class": "item"})
            for film in film_list:
                film_description = film.findAll("span")
                if len(film_description) <= 1:
                    continue

                film_duration_in_minutes = int(film_description[1].string.split(" ")[0])
                wasted_time = wasted_time + film_duration_in_minutes

            return wasted_time
        except BaseException:
            print("Something gone wrong.")
            return 0

    @staticmethod
    def _check_that_is_captcha(html):
        captcha_element = html.find_all("a", {"href": "//yandex.ru/support/captcha/"})
        return len(captcha_element) > 0

    @staticmethod
    def _check_that_is_end_of_film_list(html):
        error_element = html.find_all("div", {"class": "error-page__container-left"})
        return len(error_element) > 0
