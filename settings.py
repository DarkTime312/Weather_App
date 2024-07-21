from typing import Final

API_KEY: Final[str] = '288467633cb6e715fc2c24b28a96e742'
BASE_URL: Final[str] = 'https://api.openweathermap.org/data/2.5/forecast?'
FONT: Final[str] = 'Calibri'
TODAY_TEMP_FONT_SIZE: Final[int] = 50
SMALL_FONT_SIZE: Final[int] = 15
REGULAR_FONT_SIZE: Final[int] = 20
ANIMATION_SPEED: Final[int] = 50
ANIMATION_PAUSE_TIME: Final[float] = 0.1

WEATHER_DATA: dict = {
    'Clear': {'main': '#FFF2D1', 'title': 0x00D1F2FF, 'text': '#bd6a1f', 'divider color': '#f2eddf',
              'path': 'animations/clear'},
    'Rain': {'main': '#3079FF', 'title': 0x00FF7930, 'text': '#c1e1ff', 'divider color': '#c1c1c1',
             'path': 'animations/rain'},
    'Snow': {'main': '#3079FF', 'title': 0x00FF7930, 'text': '#c1e1ff', 'divider color': '#c1c1c1',
             'path': 'animations/snow'},
    'Clouds': {'main': '#F7F7F7', 'title': 0x00F7F7F7, 'text': '#7a8aa5', 'divider color': '#d9d9d9',
               'path': 'animations/cloudy'},
    'Thunderstorm': {'main': '#F7F7F7', 'title': 0x00F7F7F7, 'text': '#e19329', 'divider color': '#e6e6e6',
                     'path': 'animations/thunder'},
}
