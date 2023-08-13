import re

pattern = r'(?i)@remindMe\s*(?:(?:(\d+)\s*years?)?\s*)?(?:(\d+)\s*months?)?\s*(?:(\d+)\s*weeks?)?\s*(?:(\d+)\s*days?)?\s*(?:(\d+)\s*hours?)?\s*(?:(\d+)\s*minutes?)?'

tests: list[str] = list([
    "@remindMe 3 years 2 months 1 weeks 1 day",
    "@remindMe 6 months 2 days",
    "@remindMe 7 months 1 day",
    "@remindMe 2 weeks",
    "@remindMe 1 day",
    "@remindMe 2 days",    
    "@remindMe 1 hour",
    "@remindMe 2 weeks 3 hours"
])

for test in tests:
    print(f"test: {test}")
    matches = re.search(pattern, test)

    if matches:
        years, months, weeks, days, hours, minutes = matches.groups()
        print(f"Years: {years}, Months: {months}, Weeks: {weeks}, Days: {days}, Hours: {hours}, Minutes: {minutes}")
    else:
        print("No match found.")
