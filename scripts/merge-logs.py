events = {}
with open('../logs/testing.log') as logfile:
    for line in logfile:
        bits = line.split('-')
        events[bits[0]] = bits[1:]
print(events)