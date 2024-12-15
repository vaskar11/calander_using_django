import ephem
from datetime import date
import calendar
from converter.info import bs_years_data as check_dict



# Nepali week names
nepali_weekdays = ["सोमबार", "मंगलबार", "बुधबार", "बिहीबार", "शुक्रबार", "शनिबार","आइतबार"]

# Special events dictionary
IMPORTANT_EVENTS = {
    (1, 1): "नयाँ वर्ष", (1, 11): "लोकतन्त्र दिवस", (1, 18): "विश्व मजदुर दिवस",
    (1, 30): "श्रीपञ्चमी", (3, 8): "महिला दिवस", (5, 15): "कुशे औंशी",
    (6, 3): "संबिधान दिवस", (6, 8): "विश्व वातावरण दिवस", (6, 11): "गणेश चतुर्थी",
    (7, 1): "विश्व पर्यटन दिवस", (9, 1): "विश्व पर्यटन दिवस", (9, 7): "उधौली पर्व",
    (9, 12): "मोहनी नख", (9, 15): "अन्नपूर्ण यात्रा", (9, 23): "यमरी पुन्ही",
    (10, 1): "माघे संक्रान्ति", (11, 7): "प्रजातन्त्र दिवस"
}


# Tithi list for reference
TITHI_LIST = {
    1: "प्रतिपदा", 2: "द्वितीया", 3: "तृतीया", 4: "चतुर्थी", 5: "पञ्चमी",
    6: "षष्ठी", 7: "सप्तमी", 8: "अष्टमी", 9: "नवमी", 10: "दशमी",
    11: "एकादशी", 12: "द्वादशी", 13: "त्रयोदशी", 14: "चतुर्दशी", 15: "पूर्णिमा",
    16: "प्रतिपदा", 17: "द्वितीया", 18: "तृतीया", 19: "चतुर्थी", 20: "पञ्चमी",
    21: "षष्ठी", 22: "सप्तमी", 23: "अष्टमी", 24: "नवमी", 25: "दशमी",
    26: "एकादशी", 27: "द्वादशी", 28: "त्रयोदशी", 29: "चतुर्दशी", 30: "औंसी"
}


def get_tithi(date_in):
    observer = ephem.Observer()
    observer.date = ephem.Date(date_in)
    sun = ephem.Sun(observer)
    moon = ephem.Moon(observer)
    solar_longitude = sun.hlon
    lunar_longitude = moon.hlon
    tithi = int((lunar_longitude - solar_longitude) % (2 * ephem.pi) / (ephem.pi / 15)) + 1
    paksha = "शुक्लपक्ष" if tithi <= 15 else "कृष्णपक्ष"
    return TITHI_LIST.get(tithi, "Unknown"), paksha

def create_nepali_calendar(year, month, start_day_index):
    weekdays = ["आइत", "सोम", "मंगल", "बुध", "बिही", "शुक्र", "शनि"]
    months = ["बैशाख", "जेष्ठ", "अषाढ़", "श्रावण", "भाद्र", "आश्विन",
              "कार्तिक", "मंसिर", "पौष", "माघ", "फाल्गुन", "चैत्र"]
    days_in_month = check_dict[year][month - 1]
    calendar_grid = []
    week = [" "] * (start_day_index+1)

    for day in range(1, days_in_month + 1):
        week.append(str(day))
        if len(week) == 7:
            calendar_grid.append(week)
            week = []
    if week:
        while len(week) < 7:
            week.append(" ")
        calendar_grid.append(week)

    return {
        "calendar": calendar_grid,
        "month_name": months[month - 1],
        "weekdays": weekdays
    }

def calculate_nepali_date(engYear, engMonth, engDate):
    start_eng_date = date(1944, 1, 1)
    start_nep_date = (2000, 9, 17)
    day_of_week = calendar.SATURDAY

    date_provided = date(engYear, engMonth, engDate)
    diff = (date_provided - start_eng_date).days

    nep_year, nep_month, nep_day = start_nep_date
    weekday_index = day_of_week

    while diff != 0:
        days_in_month = check_dict[nep_year][nep_month - 1]
        nep_day += 1
        if nep_day > days_in_month:
            nep_month += 1
            nep_day = 1
        if nep_month > 12:
            nep_year += 1
            nep_month = 1
        weekday_index = (weekday_index + 1) % 7
        diff -= 1

    event = IMPORTANT_EVENTS.get((nep_month, nep_day), "No special event")
    nep_week_day = nepali_weekdays[weekday_index]

    tithi, paksha = get_tithi(date(engYear, engMonth, engDate))
    start_day_index = weekday_index - (nep_day - 1) % 7
    if start_day_index < 0:
        start_day_index += 7

    calendar_data = create_nepali_calendar(nep_year, nep_month, start_day_index)

    return {
        "nep_date": f"{nep_year}/{nep_month}/{nep_day}",
        "weekday": nep_week_day,
        "tithi": f"{tithi}, {paksha}",
        "event": event,
        "calendar_data": calendar_data
    }
