class Product:

    def __init__(self, iid="", name="", brand="", model="", description="", remains="", price=""):
        self.iid = iid
        self.name = name
        self.brand = brand
        self.model = model
        self.description = description
        self.remains = remains
        self.price = price

    def get_iid(self):
        return self.iid

    def get_name(self):
        return self.name

    def get_brand(self):
        return self.brand

    def get_model(self):
        return self.model

    def get_description(self):
        return self.description

    def get_remains(self):
        return self.remains

    def get_price(self):
        return self.price

    def set_name(self, name):
        self.name = name

    def set_brand(self, brand):
        self.brand = brand

    def set_model(self, model):
        self.model = model

    def set_description(self, description):
        self.description = description

    def set_remains(self, remains):
        self.remains = remains

    def set_price(self, price):
        self.price = price

    def __str__(self) -> str:
        return f"[{self.iid}," \
               f" {self.name}," \
               f" {self.brand}," \
               f" {self.model}," \
               f" {self.description}," \
               f" {self.remains}," \
               f" {self.price}]"



