import csv
import re
def CSV(archivoCsv):
    reNombre = re.compile("[a-zA-Z]+")
    name = 'IPCMUSIC/'+archivoCsv
    with open(name) as f:
        reader = csv.reader(f)
        for row in reader:
            # print(reNombre.fullmatch("asiuss oo"))
            if reNombre.fullmatch(row[0]) is not None:
                print(row[0])
                print('cumple')
            else:
                print(row[0])
                print('no cumple')
            
            print(f'{row[0]}, {row[1]}, {row[2]}, {row[3]}, {row[4]}, {row[5]}, {row[6]}')
    return [True]