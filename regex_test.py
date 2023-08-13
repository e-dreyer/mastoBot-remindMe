import re
import datetime

pattern = r'(?i)<span class="h-card"><a href="https://techhub\.social/@remindMe" class="u-url mention">@<span>remindMe</span></a></span>\s*(?:(?:(\d+)\s*years?)?\s*)?(?:(\d+)\s*months?)?\s*(?:(\d+)\s*weeks?)?\s*(?:(\d+)\s*days?)?\s*(?:(\d+)\s*hours?)?\s*(?:(\d+)\s*minutes?)?'

tests = [
    '<p><span class="h-card"><a href="https://techhub.social/@remindMe" class="u-url mention">@<span>remindMe</span></a></span> 2 weeks 3 days 10 minutes</p>'
]

for test in tests:
    print(f"test: {test}")
    matches = re.search(pattern, test)
    time_now = datetime.datetime.now()

    if matches:
        years, months, weeks, days, hours, minutes = map(lambda x: int(x or 0), matches.groups())
        print(f"Years: {years}, Months: {months}, Weeks: {weeks}, Days: {days}, Hours: {hours}, Minutes: {minutes}")
        
        delta = datetime.timedelta(
            days=days + weeks * 7 + months * 30 + years * 365,
            hours=hours,
            minutes=minutes
        )
        
        future_time = time_now + delta
        print(f"Current Time: {time_now}")
        print(f"Future Time: {future_time}")
    else:
        print("No match found.")
