import sqlite3

conn = sqlite3.connect('C:/Utils/Webb/instance/website.db')
cursor = conn.cursor()
query = "SELECT id, brand, model, color, material_up, material_down, season, sports, size, text, price FROM product"
cursor.execute(query)
sneakers_data = cursor.fetchall()
cursor.close()
conn.close()
sneakers_list = []
for sneaker in sneakers_data:
    sneakers_dict = {
        'id': sneaker[0],
        'brand': sneaker[1],
        'model': sneaker[2],
        'color': sneaker[3],
        'material_up': sneaker[4],
        'material_down': sneaker[5],
        'season': sneaker[6],
        'sports': sneaker[7],
        'size': sneaker[8],
        'price': sneaker[9],
        'text': sneaker[10]
    }
    sneakers_list.append(sneakers_dict)
