from flask import Flask, request, jsonify, make_response
import pandas as pd
import json
import numpy as np

app = Flask(__name__)


class Restaurant:
    availability = "No Disponible"
    rating = "No Popular"

    def __init__(self, name, price, popularity, quorum, tipo, rating, description):
        self.name = name
        self.price = price
        self.popularity = popularity 
        self.quorum = quorum  
        self.tipo = tipo
        self.rating = rating
        self.description = description

def cargarExcel(tipo, precio):

  xl = pd.ExcelFile("restaurantes.xlsx")
  df = xl.parse("Sheet1")

  return df.loc[(df['tipo'] == tipo)&(df['price'] == precio)]

def parseToJSON(dataFrame):
  d = [ 
    dict([
        (colname, row[i]) 
        for i,colname in enumerate(dataFrame.columns)
    ])
    for row in dataFrame.values
  ]
  return json.dumps(d)


@app.route('/restaurants', methods=['GET'])
def create_user():
  data = request.get_json()

  tipo = data['tipo']
  precio = data['price']

  df = cargarExcel(tipo, precio)
  jsondf = parseToJSON(df)
  # jsonloads = json.loads(jsondf)

  response = make_response(jsondf)
  response.headers['content-type'] = 'application/json'
  return response


# def main():

#   df = cargarExcel('internacional', 'economico')
#   jsondf = parseToJSON(df)
#   jsonloads = json.loads(jsondf)

#   print(type(jsonloads))

#   restaurants = []
#   for item in jsonloads:
#     restaurant = Restaurant(
#       item['name'],
#       item['price'],
#       item['popularity'],
#       item['quorum'],
#       item['tipo'],
#       item['rating'],
#       item['description']
#     )

#     restaurants.append(restaurant)

#     print(len(restaurants))


# if __name__ == '__main__':
#   main()
if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0')