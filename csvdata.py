import pandas as pd

colnames = ['Beverage', 'Snack', 'MainCourse', 'Other']
data = pd.read_csv('dishes.csv', names=colnames)


Beverages = data.Beverage.dropna(axis=0, how='any').tolist()
Snacks = data.Snack.dropna(axis=0, how='any').tolist()
MainCourses = data.MainCourse.dropna(axis=0, how='any').tolist()
Others = data.Other.dropna(axis=0, how='any').tolist()

# print(Beverages)
# print(Snacks)
# print(MainCourses)
# print(Others)
