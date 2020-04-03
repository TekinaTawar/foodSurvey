import json


def getdishes(ftype='', food_pref='NON-VEG'):
    with open('.//static//assets//data.json', 'r') as file:
        rows = json.load(file)

    ls = []

    for row in rows:
        if row["ftype"] == ftype:
            ls.append(row)
    rows = ls
    ls = []
    for row in rows:
        if food_pref == 'NON-VEG':
            ls.append(row["dishes"])
        elif food_pref == 'VEG':
            if row["food_pref"] == 'VEG' or row["food_pref"] == 'BOTH':
                ls.append(row["dishes"])
        elif food_pref == 'EGG':
            if row["food_pref"] == 'VEG' or row["food_pref"] == 'BOTH' or row["food_pref"] == 'EGG':
                ls.append(row["dishes"])
    return ls
