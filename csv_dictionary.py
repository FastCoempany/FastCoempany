import csv

data_dict = {}

with open('/Users/antaeus.coe/Desktop/dbase_slack_alerts/messagesfinal1019pm.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)  # This skips the header row
    for row in reader:
        url = row[0]  # Assuming URL is in the first column
        description = row[1]  # Assuming description is in the second column
        data_dict[url] = description

print(data_dict)
