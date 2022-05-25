# -*- coding: utf-8 -*-

import sqlite3

product_db_path = "/home/administrador/mwpos_server/genesis/data/server/databases/product.db"
# product_db_path = "C:\Projects\BurgerKing\MWPOS\Env1\data\server\databases\product.db"

navigation = {
    "Combos": {"NavId": 2, "SortOrder": 1, "ButtonColor": "#FFD700", "Products": [1051, 6000268]},
    "Individuais": {"NavId": 3, "SortOrder": 2, "ButtonColor": "#FFA07A", "Products": [9008, 1050, 6012]}
}

coupons_to_fix = [6000000, 6100000]


def build_navigation():
    query = "INSERT OR REPLACE INTO Navigation(NavId, Name, ParentNavId, SortOrder, ButtonText, ButtonColor) " \
            "VALUES (1, 'BK Menu', NULL, 0, 'BK Menu', NULL);"
    for nav in navigation:
        query += "\nINSERT OR REPLACE INTO Navigation(NavId, Name, ParentNavId, SortOrder, ButtonText, ButtonColor) " \
                 "VALUES ('{}', '{}', 1, '{}', '{}', '{}');" \
            .format(navigation[nav]["NavId"], nav, navigation[nav]["SortOrder"], nav, navigation[nav]["ButtonColor"])

    execute_query(query)


def build_product_navigation():
    query = ""
    for nav in navigation:
        for product_code in navigation[nav]["Products"]:
            query += "INSERT OR REPLACE INTO ProductNavigation(NavId, ClassCode, ProductCode) VALUES ('{}', 1, '{}');" \
                .format(navigation[nav]["NavId"], product_code)

    execute_query(query)


def fix_coupon_default_qty():
    query = ""
    for coupon in coupons_to_fix:
        query += "UPDATE ProductPart SET DefaultQty = '0' WHERE PartCode = '{}';".format(coupon)

    execute_query(query)


def execute_query(query):
    connection = None
    try:
        connection = sqlite3.connect(product_db_path)
        connection.executescript(query)
        connection.commit()
    except Exception as ex:
        print ex
        if connection:
            connection.rollback()
    finally:
        if connection:
            connection.close()


build_navigation()
build_product_navigation()
fix_coupon_default_qty()
