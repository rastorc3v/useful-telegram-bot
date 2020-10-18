from emoji import emojize


def em(em_code):
    return emojize(em_code, use_aliases=True)


def get_em():
    return {'cloud': em(':cloud:'),
            'moon': em(':new_moon:'),
            'sunrise': em(':sunrise:'),
            'sunset': em(':'),
            'cloud_rain': em(':cloud_with_rain:'),
            'calendar': em(':spiral_calendar_pad:'),
            'clock': em(':alarm_clock:'),
            'megaphone': em(':loudspeaker:'),
            'org': em(':speech_balloon:'),
            'link': em(':link:'),
            'weath': em(':white_sun_behind_cloud_with_rain:'),
            'oven': em(':aries:'),
            'telec': em(':taurus:'),
            'blizneci': em(':gemini:'),
            'rak': em(':cancer:'),
            'lev': em(':leo:'),
            'deva': em(':virgo:'),
            'vesi': em(':libra:'),
            'scorpion': em(':scorpius:'),
            'strelec': em(':sagittarius:'),
            'kozerog': em(':capricorn:'),
            'vodoley': em(':aquarius:'),
            'ribi': em(':pisces:')}
