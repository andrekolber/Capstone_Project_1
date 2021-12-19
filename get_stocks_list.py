def request_stock_list():
    """Return list of all stocks"""

    url = f"{API_BASE_URL}/stock/list?apikey={SECRET_KEY}"

    response = requests.get(url)
    r = response.json()

    return r


def add_stocks_to_db():
    r = request_stock_list()
    for i in range(len(r)):
        stock = Stock(
            symbol=r[i]['symbol'],
            name=r[i]['name'],
            exchange=r[i]['exchange'],
            type=r[i]['type']
        )

        db.session.add(stock)
        db.session.commit()