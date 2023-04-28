import os
from app import db, Product, app

app.app_context().push()


def save_to_db(record):
    brand = record[0]
    model = record[1]
    color = record[2]
    material_up = record[3]
    material_down = record[4]
    season = record[5]
    sports = record[6]
    size = record[7]
    text = record[8]
    price = record[9]

    product = Product(brand=brand, model=model, color=color, material_up=material_up, material_down=material_down,
                      season=season, sports=sports,
                      size=size, text=text, price=price)

    # try:
    db.session.add(product)
    db.session.commit()
    # except:
    # print("При добавлении статьи прозошла ошибка")
    # print() #::::


folder = r"C:\Users\trofi\PycharmProjects\Webb\static\pict\product"
paths = os.listdir(folder)


def fill(file):
    """
    функция извлекает из файла в массив по разделителю enter
    c
    """
    f = open(file)
    str1 = f.read()
    res = str1.split("\n")
    f.close()
    return res


list_folders = []

for i in range(len(paths)):
    if os.path.isdir(folder + "\\" + paths[i]):
        list_folders.append(folder + "\\" + paths[i])

for i in range(len(list_folders)):
    f = list_folders[i]
    lst_f = os.listdir(f)

    if "description" in lst_f:
        descr = os.listdir(f + "\\description")
        arr_desr_brand = []
        for j in range(len(descr)):
            file = f + "\\description\\" + descr[j]
            arr_desr_brand.append(fill(file))

            # print(file)
        # print(arr_desr_brand) #тут будем записывать базу данных

        for elem in range(len(arr_desr_brand)):
            save_to_db(arr_desr_brand[elem])

        print()
