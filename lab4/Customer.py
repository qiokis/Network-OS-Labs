class Customer:

    def __init__(self, iid="", name="", address=""):
        self.iid = iid
        self.name = name
        self.address = address

    def get_iid(self):
        return self.iid

    def set_address(self, address):
        self.address = address

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def get_address(self):
        return self.address

    def __str__(self) -> str:
        return f"[{self.iid}," \
               f" {self.name}," \
               f" {self.address}]"
