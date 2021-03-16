import DAO
import Product
import Customer
import Order


class Service:
    # DB_HOST = "127.0.0.1"
    # DB_NAME = "lab4"
    # DB_USER = "postgres"
    # DB_PASS = "q1i9o9k9i"
    def __init__(self):
        self.dao = DAO.DAO("lab4",
                           "127.0.0.1",
                           "postgres",
                           "q1i9o9k9i")
        self.products = {}
        self.customers = {}
        self.orders = {}
        self.dao.raise_connection()
        self.create_objects()

    def create_objects(self):
        self.products = {}
        self.customers = {}
        self.orders = {}

        for value in self.dao.get_values("products"):
            self.products.update({value[0]: Product.Product(iid=value[0],
                                                            name=value[1],
                                                            brand=value[2],
                                                            model=value[3],
                                                            description=value[4],
                                                            price=value[5],
                                                            remains=value[6])})

        for value in self.dao.get_values("orders"):
            values = [value[0], value[1], value[2]]
            product_id = value[3]
            customer_id = value[5]
            values += self.dao.get_values_by_request("select name, address from customers"
                                                     f" where id={customer_id};")[0]
            temp_values = self.dao.get_values_by_request(f"select product_name, brand_name, "
                                                         f"model_name, price from products "
                                                         f"where id={product_id};")[0]
            price = temp_values[-1]
            values += temp_values + (value[4], value[4] * price)
            self.orders.update({value[0]: Order.Order(iid=values[0],
                                                      number=values[1],
                                                      date=values[2],
                                                      customer_name=values[3],
                                                      customer_address=values[4],
                                                      product_name=values[5],
                                                      brand_name=values[6],
                                                      model_name=values[7],
                                                      price=values[8],
                                                      received=values[9],
                                                      total=values[10],
                                                      customer_id=customer_id,
                                                      product_id=product_id)})

        for value in self.dao.get_values("customers"):
            self.customers.update({value[0]: Customer.Customer(iid=value[0],
                                                               name=value[1],
                                                               address=value[2])})

    def get_products(self):
        return self.products

    def get_customers(self):
        return self.customers

    def get_orders(self):
        return self.orders

    def subtract_products(self, iid, quantity):
        quantity = int(quantity)
        if self.products[iid].get_remains() >= quantity:
            new_value = self.products[iid].get_remains() - quantity
            self.products[iid].set_remains(new_value)
            self.dao.set_values_by_request("update products\n"
                                           f"set remains={new_value}\n"
                                           f"where id={iid};")
            return 1

    def change(self, table, key, **values):
        if table == "products":
            self.products[key].set_name(values["product_name"])
            self.products[key].set_brand(values["brand_name"])
            self.products[key].set_model(values["model_name"])
            self.products[key].set_description(values["description"])
            self.products[key].set_remains(values["remains"])
            self.products[key].set_price(values["price"])
        if table == "customers":
            self.customers[key].set_name(values["name"])
            self.customers[key].set_address(values["address"])
        self.dao.change(table, key, **values)
        self.create_objects()

    def add(self, table, **values):
        self.dao.add_values(table, **values)
        self.create_objects()

    def sort_orders(self, table_to_update, type=""):
        sorted_dict = {}
        keys = list(self.orders.keys())
        keys = sorted(keys)
        if type == "order":
            for i in keys:
                sorted_dict.update({i: self.orders[i]})
            self.orders = sorted_dict
        elif type == "client":
            customers = []
            for i in self.orders.values():
                if not i.get_customer_name() in customers:
                    customers.append(i.get_customer_name())
            customers = sorted(customers)
            for i in customers:
                for j, key in zip(self.orders.values(), self.orders.keys()):
                    if i == j.get_customer_name():
                        sorted_dict.update({key: j})
            self.orders = sorted_dict
        elif type == "product":
            products = []
            for i in self.orders.values():
                if not i.get_product_name() in products:
                    products.append(i.get_product_name())
            products = sorted(products)
            for i in products:
                for j, key in zip(self.orders.values(), self.orders.keys()):
                    if i == j.get_product_name():
                        sorted_dict.update({key: j})
            self.orders = sorted_dict
        table_to_update.update_table()

    def delete(self, table, iid):
        if table == "products":
            del self.products[int(iid)]
            self.dao.del_value(table, iid)
            zipper = zip(self.orders.copy().keys(), self.orders.copy().values())
            for key, value in zipper:
                if value.get_product_id() == iid:
                    self.delete("orders", key)
        elif table == "orders":
            del self.orders[int(iid)]
            self.dao.del_value(table, iid)
        elif table == "customers":
            del self.customers[int(iid)]
            self.dao.del_value(table, iid)
            zipper = zip(self.orders.copy().keys(), self.orders.copy().values())
            for key, value in zipper:
                if value.get_customer_id() == iid:
                    self.delete("orders", key)


if __name__ == '__main__':
    s = Service()
    s.create_objects()
    s.sort_orders("product")
