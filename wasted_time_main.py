import sys
from kinopoisk_parser import KinopoiskParser
from proxy_manager import ProxyManager


if __name__ == "__main__":
    if len(sys.argv) > 1:
        user_id = sys.argv[1]
    else:
        raise Exception("Enter you kinopoisk user id")

    new_proxy_manager = ProxyManager()
    kinopoisk_parser = KinopoiskParser(user_id)

    kinopoisk_parser.calculate_wasted_time(new_proxy_manager)

    time_in_minute = int(kinopoisk_parser.get_wasted_time())

    print(f'You wasted {round(time_in_minute, 2)} minutes or {round(time_in_minute / 60, 2)} hours or {round(time_in_minute / 60 / 24, 2)} day')
