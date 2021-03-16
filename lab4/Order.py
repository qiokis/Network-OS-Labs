class Order:
    # TODO Переделать
    def __init__(self, iid="", number="", date="",
                 customer_name="", customer_address="",
                 product_name="", brand_name="", model_name="",
                 price="", received="", total="", customer_id="", product_id=""):
        self.iid = iid
        self.number = number
        self.date = date
        self.received = received
        self.customer_name = customer_name
        self.customer_address = customer_address
        self.product_name = product_name
        self.brand_name = brand_name
        self.model_name = model_name
        self.price = price
        self.total = total
        self.product_id = product_id
        self.customer_id = customer_id

    def set_number(self, number):
        self.number = number

    def set_date(self, date):
        self.date = date

    def set_received(self, received):
        self.received = received

    def set_customer_name(self, customer_name):
        self.customer_name = customer_name

    def set_customer_address(self, customer_address):
        self.customer_address = customer_address

    def set_product_name(self, product_name):
        self.product_name = product_name

    def set_brand_name(self, brand_name):
        self.brand_name = brand_name

    def set_model_name(self, model_name):
        self.model_name = model_name

    def set_price(self, price):
        self.price = price

    def set_total(self, total):
        self.total = total

    def get_iid(self):
        return self.iid

    def get_number(self):
        return self.number

    def get_date(self):
        return self.date

    def get_received(self):
        return self.received

    def get_customer_name(self):
        return self.customer_name

    def get_customer_address(self):
        return self.customer_address

    def get_product_name(self):
        return self.product_name

    def get_brand_name(self):
        return self.brand_name

    def get_model_name(self):
        return self.model_name

    def get_price(self):
        return self.price

    def get_total(self):
        return self.total

    def get_customer_id(self):
        return self.customer_id

    def get_product_id(self):
        return self.product_id

    def __str__(self) -> str:
        return f"[{self.iid}," \
               f" {self.number}," \
               f" {self.date}," \
               f" {self.received}," \
               f" {self.customer_name}," \
               f"{self.customer_address}," \
               f"{self.product_name}," \
               f"{self.brand_name}," \
               f"{self.model_name}," \
               f"{self.price}," \
               f"{self.total}]"
