import time
import xml.etree.ElementTree as ET

tree = ET.parse('MercanPerde_05122021_195231.xml')
products = tree.getroot()


# for product in range(len(products)):
#     variant_length = len(products[product][13])
#     for i in range(variant_length):
#         variant_detail_len = len(products[product][13][i])
#         variant_stocks = products[product][13][i]
#         name = products[product][2]
#         unit_price = products[product][8].text
#         discount_rate = products[product][15].text
#         # each_variant_detail = root[x][13][i][j]
#         print(products[product][2].text)
#         print('Birim Fiyat: ', products[product][8].text)
#         print('İndirim Oranı: ', products[product][15].text)
#         for j in range(variant_detail_len):
#             if (products[product][13][i][j].tag == "Ozellik"):
#
#                 try:
#                     print(products[product][13][i][j].tag, ':', products[product][13][i][j].get('isim'), '=',
#                           products[product][13][i][j].text)
#
#                 except:
#                     print(products[product][13][i][j].tag, ':', products[product][13][i][j].text)
#         print("-----------------------")
#
#     print("*********************************************\n \n")


# list = []
# for stok in root.iter('Stoklar'):
#     for each in stok.find('Stok'):
#         print(each.text)
#         list.append(each)

class Curtain():

    def __init__(self, name, unit_price, discount_rate):
        self.name = name
        self.unit_price = unit_price
        self.discount_rate = discount_rate
        self.variant_list = []

    def set_variant_width_to_int(self):
        for var in self.variant_list:
            try:
                var.width = int(var.width)
            except:
                pass  # print("Bu genişlik seçeneği int yapılamıyor: ", self.name, " ", var.width, " type ", type(var.width))

    def set_variant_quantity(self, new_quantity):
        for variant in self.variant_list:
            variant.set_quantity(new_quantity)

    def set_unit_price(self, price):
        self.unit_price = price

    def set_discount_rate(self, rate):
        self.discount_rate = rate

    def set_variant_prices(self, new_unit_price, new_discount_rate):

        for variant in self.variant_list:
            self.unit_price = new_unit_price
            self.discount_rate = new_discount_rate
            if variant.pile == '0':
                print("Varyant Bilgisi veya Fiyat Tanımsız")
            else:

                try:
                    if "yüksek gramajlı" in variant.fabric.lower():
                        self.unit_price += 10
                    if "sık pile" in variant.pile.lower():
                        variant.price = round(
                            self.unit_price * 3 * variant.width // 100 * (1 - self.discount_rate / 100))
                    elif "orta pile" in variant.pile.lower():
                        variant.price = round(
                            self.unit_price * ((2.5 * variant.width) + 20) // 100 * (1 - self.discount_rate / 100))
                    elif "seyrek pile" in variant.pile.lower():
                        variant.price = round(
                            self.unit_price * ((2 * variant.width) + 20) // 100 * (1 - self.discount_rate / 100))
                    elif "pilesiz" in variant.pile.lower():
                        if type(variant.width) == str and "numune" in variant.width.lower():
                            variant.price = round(self.unit_price * (1 - self.discount_rate / 100))
                        elif int(variant.width) < 80:
                            variant.price = round(self.unit_price * (1 - self.discount_rate / 100))
                        else:
                            variant.price = round(
                                (self.unit_price * (variant.width + 35)) / 100 * (1 - self.discount_rate / 100))


                except:
                    printed_list = []
                    printed_list.append(self.name)
                    if self.name not in printed_list:
                        print(self.name, " ürün varyantı tam sayı")


class Variant():
    price = 0
    width = 0
    pile = 0
    fabric = 0
    quantity = 0

    def set_quantity(self, new_quantity):
        self.quantity = new_quantity


class Products():

    def __init__(self):
        self.product_list = []

    def set_each_product_prices(self):
        self.show_list(self.product_list)
        print(
            "Önce ürün fiyatı sonra indirim oranını sonra adet sayısını arada bir boşluk olucak şekilde giriniz: ")

        for product_index in range(len(self.product_list)):
            values = input(f"[{product_index + 1}] {self.product_list[product_index].name} : ")
            values = values.split(" ")

            self.set_variant_prices(self.product_list[product_index].name, int(values[0]), int(values[1]),
                                    int(values[2]))

    def set_variant_prices(self, name, new_price, discount_rate):
        for x in self.product_list:
            if x.name == name:
                x.set_variant_width_to_int()
                # function thats in curtain class
                x.set_variant_prices(new_price, discount_rate)
        return self.product_list

    def set_variant_prices(self, name, new_price, discount_rate, new_quantity):
        for x in self.product_list:
            if x.name == name:
                x.set_variant_width_to_int()
                x.set_variant_quantity(new_quantity)
                # function thats in curtain class
                x.set_variant_prices(new_price, discount_rate)
        print(len(self.product_list))

        return self.product_list

    def get_products_list(self):
        for i in self.product_list:
            print(i.name, " ", i.unit_price, " ", i.discount_rate)

    def add_to_product_list(self, products_xml):

        for product in range(len(products_xml)):
            variant_length = len(products_xml[product][13])

            name = products_xml[product][2].text
            unit_price = products_xml[product][8].text
            discount_rate = products_xml[product][15].text
            prod = Curtain(name, unit_price, discount_rate=discount_rate)

            for i in range(variant_length):
                variant_detail_len = len(products_xml[product][13][i])
                variant_stocks = products_xml[product][13][i]

                # each_variant_detail = root[x][13][i][j]

                # print(products[product][2].text)
                # print('Birim Fiyat: ', products[product][8].text)
                # print('İndirim Oranı: ', products[product][15].text)
                var = Variant()
                for j in range(variant_detail_len):

                    if (products_xml[product][13][i][j].tag == "Ozellik"):

                        if products_xml[product][13][i][j].get('isim') == "Kumaş Seçiniz":
                            var.fabric = products[product][13][i][j].text

                        if products_xml[product][13][i][j].get('isim') == "En" or products_xml[product][13][i][j].get(
                                'isim') == "En Seçiniz":
                            var.width = products[product][13][i][j].text

                        if products_xml[product][13][i][j].get('isim') == "Pile" or products_xml[product][13][i][
                            j].get('isim') == "Pile Seçiniz:" or products_xml[product][13][i][j].get(
                            'isim') == "Pile Seçiniz":
                            var.pile = products_xml[product][13][i][j].text
                    if products_xml[product][13][i][j].tag == 'Miktar':
                        var.quantity = products_xml[product][13][i][j].text
                    # if products_xml[product][13][i][j].tag == "StokFiyatı":
                    #     var.price = products_xml[product][13][i][j].text
                if int(var.price) != 0 or var.pile != 0 or int(var.width) != 0:
                    prod.variant_list.append(var)

                # print(prod.name, prod.variant_list)
            self.product_list.append(prod)

    def set_products_into_xml(self, products_xml_root, products_list):
        pass

    def __str__(self):

        for prod in self.product_list:
            if len(prod.variant_list) > 200:
                print(prod.name, "\t", prod.unit_price, "\t", prod.discount_rate)
                for variant in prod.variant_list:
                    # if variant.width == 0 and variant.pile == 0 and variant.price == 0:
                    #     if prod.name not in procedured:
                    #         procedured.append(prod.name)
                    #         print("#####################################\n")
                    #         print(prod.name)
                    print(variant.width, "\t", variant.pile, "\t \t", variant.price, "\t", variant.quantity, "\t",
                          variant.fabric)

    def take_product_list_and_details(self):
        product_list = []

        while True:

            for product_index in range(len(self.product_list)):
                print(f"[{product_index + 1}] {self.product_list[product_index].name} ")

            print("Çıkmak için 'X' tuşuna basınız...")
            print("Seçtiğiniz ürünleri göstermek için 0'a basınız: ")
            product_index_flist = input(
                "Lütfen Fiyatını Değiştirmek istediğiniz ürünün id'sini, yeni fiyat bilgisini ve dilerseniz güncellemek istediğiniz stok sayısını giriniz: ")

            if product_index_flist.lower() == 'x':
                self.product_list = product_list
                break

            elif product_index_flist == "0" or product_index_flist == 0:
                for product_index in range(len(product_list)):
                    print(f"[{product_index + 1}] {product_list[product_index].name} ")

                input('Seçime devam Etmek için bir tuşa basınız: ')

            elif int(product_index_flist) - 1 >= len(self.product_list) or int(product_index_flist) - 1 < 0:
                product_index_flist = input(
                    "Hatalı tuşlama tekrar deneyiniz, Fiyatını Değiştirmek istediğiniz ürünün id'sini, yeni fiyat bilgisini ve dilerseniz güncellemek istediğiniz stok sayısını giriniz: ")

            else:
                product_list.append(self.product_list[int(product_index_flist) - 1])
                self.product_list.pop(int(product_index_flist) - 1)

    def show_list(self, product_list):
        for product_index in range(len(product_list)):
            print(f"[{product_index + 1}] {product_list[product_index].name} ")


if __name__ == "__main__":
    pr = Products()
    pr.add_to_product_list(products)
    # pr.set_variant_prices(150, 50, 999)
    # pr.__str__()
    pr.take_product_list_and_details()
    pr.set_each_product_prices()
    pr.__str__()
