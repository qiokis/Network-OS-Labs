import psycopg2
#
# DB_HOST = "127.0.0.1"
# DB_NAME = "lab4"
# DB_USER = "postgres"
# DB_PASS = "q1i9o9k9i"


class DAO:

    def __init__(self, db_name, db_host, user, password):
        self.__DB_HOST = db_host
        self.__DB_NAME = db_name
        self.__DB_USER = user
        self.__DB_PASS = password
        self.__connection = None
        self.__cursor = None
        self.__request = ""

    def raise_connection(self):
        self.__connection = psycopg2.connect(host=self.__DB_HOST,
                                             user=self.__DB_USER,
                                             password=self.__DB_PASS,
                                             database=self.__DB_NAME)

    def close_connection(self):
        self.__connection.close()

    def __create_cursor(self):
        self.__cursor = self.__connection.cursor()

    def __delete_cursor(self):
        self.__cursor.close()

    def get_values_by_request(self, request):
        self.__create_cursor()
        self.__cursor.execute(request)
        values = self.__cursor.fetchall()
        self.__delete_cursor()
        return values

    def set_values_by_request(self, request):
        self.__create_cursor()
        self.__cursor.execute(request)
        self.__connection.commit()
        self.__delete_cursor()

    def get_values(self, table):
        self.__create_cursor()
        self.__cursor.execute(f"Select * from {table}")
        values = self.__cursor.fetchall()
        self.__delete_cursor()
        return values

    def create_insert_request(self, table, **values):
        self.__request = f"insert into {table}\n("
        for i in values.keys():
            self.__request += f"{i},"
        self.__request = f"{self.__request[:-1]})\nvalues ("
        for i in values.values():
            self.__request += f"\'{i}\',"
        self.__request = f"{self.__request[:-1]});"

    def create_change_request(self, table, key_table, **values):
        self.__request = f"update {table}\nset\n"
        for key, value in zip(values.keys(), values.values()):
            self.__request += f"{key}=\'{value}\',"
        self.__request = f"{self.__request[:-1]}\nwhere id={key_table};"

    def add_values(self, table, **values):
        self.create_insert_request(table, **values)
        self.__create_cursor()
        self.__cursor.execute(self.__request)
        # if table_customers == "products":
        #     self.__cursor.execute("insert into {}"
        #                           " (product_name, brand_name, model_name, description, price, remains)"
        #                           " values (\'{}\', \'{}\', \'{}\', \'{}\', {}, {});"
        #                           .format(table_customers,
        #                                   values["product_name"],
        #                                   values["brand_name"],
        #                                   values["model_name"],
        #                                   values["description"],
        #                                   values["price"],
        #                                   values["remains"]
        #                                   ))
        self.__connection.commit()
        self.__delete_cursor()

    def del_value(self, table, iid):
        self.__create_cursor()
        self.__cursor.execute("delete from {} "
                              "where id={}"
                              .format(table, iid))
        self.__connection.commit()
        self.__delete_cursor()

    def change(self, table, key, **values):
        self.create_change_request(table, key, **values)
        self.__create_cursor()
        self.__cursor.execute(self.__request)
        # if table_customers == "products":
        #     self.__create_cursor()
        #     self.__cursor.execute("update {} \n"
        #                           "set product_name=\'{}\',\n"
        #                           "brand_name=\'{}\',\n"
        #                           "model_name=\'{}\',\n"
        #                           "description=\'{}\',\n"
        #                           "price={},\n"
        #                           "remains={}\n"
        #                           "where id={};"
        #                           .format(table_customers,
        #                                   values["product_name"],
        #                                   values["brand_name"],
        #                                   values["model_name"],
        #                                   values["description"],
        #                                   values["price"],
        #                                   values["remains"],
        #                                   values["iid"]))
        self.__connection.commit()
        self.__delete_cursor()

    def update(self, table):
        pass


if __name__ == '__main__':
    d = DAO("lab4", "127.0.0.1", "postgres", "q1i9o9k9i")
    d.raise_connection()
    d.add_values("products", product_name="ABC",
                 brand_name="Hitachi",
                 model_name="FGH",
                 description="good",
                 price="12",
                 remains="40")
    d.close_connection()

