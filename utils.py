def clean_price(price):
    price = price.replace("$", "")
    price = price.replace(",", "")
    return int(price)