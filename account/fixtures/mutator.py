import csv
import json


def c2json():
    with open('countries.csv', 'r') as f:
        output = []
        reader = csv.reader(f, delimiter=',')
        pk = 1
        for line in reader:
            if line[0] == 'Name':
                continue
            row = {
                'model': 'account.Country',
                'pk': pk,
                'fields': {
                    'name': line[0],
                    'code': line[1]
                }
            }
            output.append(row)
            pk += 1

        json_data = json.dumps(output, indent=2)
        fw = open('countries.json', 'w')
        fw.write(json_data)
        fw.close()
