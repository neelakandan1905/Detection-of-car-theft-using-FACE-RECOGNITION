import csv
login_count = 0

with open("C:/.....passwordfile.csv",
          'r') as readfile:
    myreader = csv.reader(readfile)
    check_list = []
    for row in myreader:
        check_list.append(row)
    readfile.close()
