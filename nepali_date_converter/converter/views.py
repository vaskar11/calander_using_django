# from django.shortcuts import render

# # Create your views here.

# from django.shortcuts import render
# from .calendar_logic import calculate_nepali_date
# # # Create your views here.

# def index(request):
#     return render(request, 'converter/index.html')

# def convert_date(request):
#     if request.method == "POST":
#         year = int(request.POST['year'])
#         month = int(request.POST['month'])
#         day = int(request.POST['day'])

#         result = calculate_nepali_date(year, month, day)
#         year_date= result["nep_date"].split('/')[0]
#         context = {
#             "nepali_date": result["nep_date"],
#             "weekday": result["weekday"],   #gives which day it is
#             "tithi": result["tithi"],
#             "event": result["event"],
#             "calendar": result["calendar_data"]["calendar"],
#             "weekdays": result["calendar_data"]["weekdays"],    #gives the list of the week for calendar
#             "month_name": result["calendar_data"]["month_name"],
#             'year_date': year_date,
#         }
#         return render(request, 'converter/result.html', context)



from django.shortcuts import render
from .calendar_logic import calculate_nepali_date

# Render the index page
def index(request):
    return render(request, 'converter/index.html')

# Handle the date conversion
def convert_date(request):
    if request.method == "POST":
        try:
            # Get input date from the form
            year = int(request.POST['year'])
            month = int(request.POST['month'])
            day = int(request.POST['day'])

            # Convert to Nepali date
            result = calculate_nepali_date(year, month, day)

            # Extract year, month, and day from result
            nepali_date_parts = result["nep_date"].split('/')
            year_date = nepali_date_parts[0]
            nep_day = nepali_date_parts[2]

            # Prepare context for the result page
            context = {
                "nepali_date": result["nep_date"],
                "weekday": result["weekday"],
                "tithi": result["tithi"],
                "event": result["event"],
                "calendar": result["calendar_data"]["calendar"],
                "weekdays": result["calendar_data"]["weekdays"],
                "month_name": result["calendar_data"]["month_name"],
                "year_date": year_date,
                "that_day": nep_day,  # Highlighted Nepali day
                "eng_day": day,  # English day of the month
            }

            return render(request, 'converter/result.html', context)

        except Exception as e:
            # Handle any conversion errors
            context = {"error": f"Error: {str(e)}"}
            return render(request, 'converter/index.html', context)

    return render(request, 'converter/index.html')
