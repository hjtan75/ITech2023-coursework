import random
startHour = 12
endHour = 20

timeslots = []
for hour in range(startHour, endHour+1):
    for minute in range(0, 31, 30):
        if hour != endHour or minute != 30:
            hourString = str(hour)
            minString = str(minute) if minute == 30 else str(minute) + "0"
            timeslots.append((f"{hourString}:{minString}", f"{hourString}:{minString}"))


timeslots = tuple(timeslots)


for i in range(5):
    print(random.choice(timeslots[0]))

