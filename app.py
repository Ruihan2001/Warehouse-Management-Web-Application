import mysql
from flask import Flask, render_template, redirect, request, url_for, session, jsonify, json
import models
import configs
from flask_sqlalchemy import SQLAlchemy, BaseQuery, SessionBase
from sqlalchemy import create_engine, extract
from sqlalchemy.orm import sessionmaker
import time, datetime
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
import mysql.connector

app = Flask(__name__)
app.config['SECRET_KEY'] = 'never guessing this!'
app.config['SQLALCHEMY_DATABASE_URI'] = configs.DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
config = {
    'user': 'root',
    'password': 'Qwe101493',
    'host': '127.0.0.1',
    'port': '3306',
    'database': 'wms_engproj'
}

con = mysql.connector.connect(user='root',
                              password='Qwe101493',
                              host='127.0.0.1',
                              port='3306',
                              database='wms_engproj',
                              auth_plugin='mysql_native_password'
                              )

mycursor = con.cursor(buffered=True)
db = SQLAlchemy(app)



class EmpUser(db.Model):
    __tablename__ = 'emp_user'

    emp_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    emp_username = db.Column(db.String(20), nullable=False)
    emp_password = db.Column(db.String(30), nullable=False)
    emp_level = db.Column(db.Integer, nullable=False)


class EmpLoginRecord(db.Model):
    __tablename__ = 'emp_login_record'

    emp_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    emp_login_time = db.Column(db.TIMESTAMP)
    emp_logout_time = db.Column(db.TIMESTAMP)


class ProductsInventory(db.Model):
    __tablename__ = 'products_Inventory'

    pro_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    pro_name = db.Column(db.String(35), nullable=False)
    pro_class = db.Column(db.String(20), nullable=False)
    pro_charge = db.Column(db.String(35), nullable=False)
    pro_region = db.Column(db.String(1), nullable=False)
    re_section = db.Column(db.Integer, nullable=False)
    pro_amount = db.Column(db.Integer, nullable=False)
    pro_remark = db.Column(db.String(50))
    pro_city = db.Column(db.String(20), nullable=False)
    sto_time = db.Column(db.DATE, nullable=False)


class ClassRegion(db.Model):
    __tablename__ = 'class_region'
    c_name = db.Column(db.String(20), nullable=False, primary_key=True)
    r_name = db.Column(db.String(1), nullable=False)
    s_cost = db.Column(db.Integer, nullable=False)
    r_budget = db.Column(db.Integer, nullable=False)


class Request(db.Model):
    __tablename__ = 'request'
    task_id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    user_id = db.Column(db.VARCHAR(20), nullable=False)
    comm_start_time = db.Column(db.DATETIME, nullable=False)
    comm_end_time = db.Column(db.DATETIME)
    alter_storage = db.Column(db.VARCHAR(120), nullable=False)
    alter_amount = db.Column(db.Integer, nullable=False)
    condition = db.Column(db.Integer, nullable=False)


class Transport(db.Model):
    __tablename__ = 'transmission'
    task_id = db.Column(db.Integer, nullable=False, primary_key=True)
    pro_name = db.Column(db.String(35), nullable=False)
    start_id = db.Column(db.Integer, nullable=False, primary_key=True)
    start_city = db.Column(db.VARCHAR(30))
    end_id = db.Column(db.Integer, nullable=False, primary_key=True)
    end_city = db.Column(db.VARCHAR(30))


# db.init_app(app)

db.create_all()


@app.route('/refresh')
def refresh(self):
    return {
        'id': self.pro_id,
        'name': self.pro_name,
        'category': self.pro_class,
        'pic': self.pro_charge,
        'region': self.pro_region,
        'region_number': self.re_section,
        'amount': self.pro_amount,
        'remarks': self.pro_remark
    }


def Create(name, clas, charge, number, amount, remark):
    item = session.query(ProductsInventory).filter(ProductsInventory.pro_name == name).first()
    if (item != None):
        item.pro_amount += amount
    else:
        region = session.query(ClassRegion).filter(ClassRegion.c_name == clas).first()
        new_pro = ProductsInventory \
            (pro_name=name, pro_class=clas, pro_charge=charge, pro_region=region.r_name, re_section=number,
             pro_amount=amount, pro_remark=remark)
        session.add(new_pro)
    session.commit()
    session.close()


def Delete(name_list):
    for i in name_list:
        de_pro = db.session.query(ProductsInventory).filter(ProductsInventory.pro_name == i).one()
        db.session.delete(de_pro)
        db.session.commit()
        db.session.close()


def Correction(id, name, clas, charge, section, remark):
    item = session.query(ProductsInventory).filter(ProductsInventory.pro_id == id).first()
    # print("It cannot be found. Please make sure your input is correct or existed")
    if name == "null":
        pass
    else:
        item.pro_name = name
    if clas == "null":
        pass
    else:
        item.pro_class = clas
        item.pro_region = session.query(ClassRegion).filter(ClassRegion.c_name == clas).first().r_name
    if charge == "null":
        pass
    else:
        item.pro_charge = charge
    if section == "null":
        pass
    else:
        item.re_section = section
    if remark == "null":
        pass
    else:
        item.pro_remark = remark
    session.commit()
    session.close()


def Search(name, clas, section, charge, remark):
    result = []
    item_list = []

    if name != "null":
        item = session.query(ProductsInventory).filter(ProductsInventory.pro_name == name).first()
        result = [item.pro_name, item.pro_class, item.pro_charge, item.pro_region, item.re_section, item.pro_amount,
                  item.pro_remark]
    elif remark != "null":
        item = session.query(ProductsInventory).filter(ProductsInventory.pro_remark.contains(remark)).first()
        result = [item.pro_name, item.pro_class, item.pro_charge, item.pro_region, item.re_section, item.pro_amount,
                  item.pro_remark]
    else:
        if clas != "null":
            if section != "null":
                item = session.query(ProductsInventory).filter(ProductsInventory.pro_class == clas).filter(
                    ProductsInventory.re_section == section).first()
                result = [item.pro_name, item.pro_class, item.pro_charge, item.pro_region, item.re_section,
                          item.pro_amount, item.pro_remark]
            else:
                if charge != "null":
                    items = session.query(ProductsInventory).filter(ProductsInventory.pro_class == clas).filter(
                        ProductsInventory.pro_charge == charge).all()
                    for i in items:
                        item_list = [i.pro_name, i.pro_class, i.pro_charge, i.pro_region, i.re_section,
                                     i.pro_amount, i.pro_remark]
                        result.append(item_list)
                else:
                    items = session.query(ProductsInventory).filter(ProductsInventory.pro_class == clas).all()
                    for i in items:
                        item_list = [i.pro_name, i.pro_class, i.pro_charge, i.pro_region, i.re_section,
                                     i.pro_amount, i.pro_remark]
                        result.append(item_list)
        else:
            if charge != "null":
                items = session.query(ProductsInventory).filter(ProductsInventory.pro_charge == charge).all()
                for i in items:
                    item_list = [i.pro_name, i.pro_class, i.pro_charge, i.pro_region, i.re_section,
                                 i.pro_amount, i.pro_remark]
                    result.append(item_list)
            else:
                return "Not found"
    return result


# This is start of the testing functions.

# 添加功能的参数分别为名称，类名，负责人，该种类仓库下的区号，数量，备注。
# Create('相机','数码产品','吕俊逸',3,5,"")

# 删除功能的参数为名称，即删除条目。
# Delete("黄鱼")

# 修改功能的参数分别为id，更改后的名字，更改后的种类，更改后的负责人，更改后的区名以及更改后的备注。
# 可以为“null”，但是不能修改数量。
# Correction(3,"苹果",'水果','张名佳',5,'7')

# 查询功能第一个参数是名字，最高优先级；第二个是类名；第三个是类名之后的地区名，不可单独查询；第四个是负责人名字；第五个是备注，次高优先级，当前为近似查询。
# 当存在名字或者（类名和地区名同时给出），返回的是唯一的列表，包含该条目所有信息；其余情况返回多个条目的二维列表。
# 不查询的参数设置为“null”。
# r = Search("null",'null','null','null','null')
# for i in r:
#   print(i)


def Select_By_Time():
    s1 = "SELECT pro_class,SUM(pro_amount)*s_cost*90,r_budget,CONCAT(round(SUM(pro_amount)*s_cost*90/r_budget*100),'%')  from products_inventory join class_region ON pro_class = c_name WHERE sto_time <= '2021-03-31' GROUP BY pro_class;"
    s2 = "SELECT pro_class,SUM(pro_amount)*s_cost*90,r_budget,CONCAT(round(SUM(pro_amount)*s_cost*90/r_budget*100),'%')  from products_inventory join class_region ON pro_class = c_name WHERE sto_time <= '2021-06-30' GROUP BY pro_class;"
    s3 = "SELECT pro_class,SUM(pro_amount)*s_cost*90,r_budget,CONCAT(round(SUM(pro_amount)*s_cost*90/r_budget*100),'%')  from products_inventory join class_region ON pro_class = c_name WHERE sto_time <= '2021-09-30' GROUP BY pro_class;"
    s4 = "SELECT pro_class,SUM(pro_amount)*s_cost*90,r_budget,CONCAT(round(SUM(pro_amount)*s_cost*90/r_budget*100),'%')  from products_inventory join class_region ON pro_class = c_name WHERE sto_time <= '2021-12-31' GROUP BY pro_class;"
    total = []
    mycursor.execute(s1)
    myresult1 = mycursor.fetchall()
    myresult1.insert(0, 1)
    total.append(myresult1)

    mycursor.execute(s2)
    myresult2 = mycursor.fetchall()
    myresult2.insert(0, 2)
    total.append(myresult2)

    mycursor.execute(s3)
    myresult3 = mycursor.fetchall()
    myresult3.insert(0, 3)
    total.append(myresult3)

    mycursor.execute(s4)
    myresult4 = mycursor.fetchall()
    myresult4.insert(0, 4)
    total.append(myresult4)
    for x in total:
        print(x)
    print(total[1][2][2])
    return total


def Select_by_category():
    final = []
    s1 = """SELECT pro_class,QUARTER('2020-03-31'),SUM(pro_amount)*s_cost*90 FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Appliances' AND sto_time <= '2021-03-31' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-06-30'),SUM(pro_amount)*s_cost*90 FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Appliances' AND sto_time <= '2021-06-30' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-09-30'),SUM(pro_amount)*s_cost*90 FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Appliances' AND sto_time <= '2021-09-30' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-12-31'),SUM(pro_amount)*s_cost*90 FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Appliances' AND sto_time <= '2021-12-31' GROUP BY pro_class,s_cost;
            """
    s2 = """SELECT pro_class,QUARTER('2020-03-31'),SUM(pro_amount)*s_cost*90 FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Books' AND sto_time <= '2021-03-31' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-06-30'),SUM(pro_amount)*s_cost*90 FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Books' AND sto_time <= '2021-06-30' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-09-30'),SUM(pro_amount)*s_cost*90 FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Books' AND sto_time <= '2021-09-30' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-12-31'),SUM(pro_amount)*s_cost*90 FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Books' AND sto_time <= '2021-12-31' GROUP BY pro_class,s_cost;
            """
    s3 = """SELECT pro_class,QUARTER('2020-03-31'),SUM(pro_amount)*s_cost*90 FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Clothing' AND sto_time <= '2021-03-31' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-06-30'),SUM(pro_amount)*s_cost*90 FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Clothing' AND sto_time <= '2021-06-30' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-09-30'),SUM(pro_amount)*s_cost*90 FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Clothing' AND sto_time <= '2021-09-30' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-12-31'),SUM(pro_amount)*s_cost*90 FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Clothing' AND sto_time <= '2021-12-31' GROUP BY pro_class,s_cost;
            """
    s4 = """SELECT pro_class,QUARTER('2020-03-31'),SUM(pro_amount)*s_cost*90 FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Daily Necessary' AND sto_time <= '2021-03-31' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-06-30'),SUM(pro_amount)*s_cost*90 FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Daily Necessary' AND sto_time <= '2021-06-30' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-09-30'),SUM(pro_amount)*s_cost*90 FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Daily Necessary' AND sto_time <= '2021-09-30' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-12-31'),SUM(pro_amount)*s_cost*90 FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Daily Necessary' AND sto_time <= '2021-12-31' GROUP BY pro_class,s_cost;
            """
    s5 = """SELECT pro_class,QUARTER('2020-03-31'),SUM(pro_amount)*s_cost*90 FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Digital Production' AND sto_time <= '2021-03-31' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-06-30'),SUM(pro_amount)*s_cost*90 FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Digital Production' AND sto_time <= '2021-06-30' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-09-30'),SUM(pro_amount)*s_cost*90 FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Digital Production' AND sto_time <= '2021-09-30' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-12-31'),SUM(pro_amount)*s_cost*90 FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Digital Production' AND sto_time <= '2021-12-31' GROUP BY pro_class,s_cost;
            """
    s6 = """SELECT pro_class,QUARTER('2020-03-31'),SUM(pro_amount)*s_cost*90 FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Fruit' AND sto_time <= '2021-03-31' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-06-30'),SUM(pro_amount)*s_cost*90 FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Fruit' AND sto_time <= '2021-06-30' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-09-30'),SUM(pro_amount)*s_cost*90 FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Fruit' AND sto_time <= '2021-09-30' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-12-31'),SUM(pro_amount)*s_cost*90 FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Fruit' AND sto_time <= '2021-12-31' GROUP BY pro_class,s_cost;
            """
    s7 = """SELECT pro_class,QUARTER('2020-03-31'),SUM(pro_amount)*s_cost*90 FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Furniture' AND sto_time <= '2021-03-31' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-06-30'),SUM(pro_amount)*s_cost*90 FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Furniture' AND sto_time <= '2021-06-30' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-09-30'),SUM(pro_amount)*s_cost*90 FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Furniture' AND sto_time <= '2021-09-30' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-12-31'),SUM(pro_amount)*s_cost*90 FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Furniture' AND sto_time <= '2021-12-31' GROUP BY pro_class,s_cost;
            """
    s8 = """SELECT pro_class,QUARTER('2020-03-31'),SUM(pro_amount)*s_cost*90 FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Medicine' AND sto_time <= '2021-03-31' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-06-30'),SUM(pro_amount)*s_cost*90 FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Medicine' AND sto_time <= '2021-06-30' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-09-30'),SUM(pro_amount)*s_cost*90 FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Medicine' AND sto_time <= '2021-09-30' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-12-31'),SUM(pro_amount)*s_cost*90 FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Medicine' AND sto_time <= '2021-12-31' GROUP BY pro_class,s_cost;
            """
    s9 = """SELECT pro_class,QUARTER('2020-03-31'),SUM(pro_amount)*s_cost*90 FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Seafood' AND sto_time <= '2021-03-31' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-06-30'),SUM(pro_amount)*s_cost*90 FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Seafood' AND sto_time <= '2021-06-30' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-09-30'),SUM(pro_amount)*s_cost*90 FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Seafood' AND sto_time <= '2021-09-30' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-12-31'),SUM(pro_amount)*s_cost*90 FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Seafood' AND sto_time <= '2021-12-31' GROUP BY pro_class,s_cost;
            """

    mycursor.execute(s1)
    myresult1 = mycursor.fetchall()
    final.append(myresult1)

    mycursor.execute(s2)
    myresult2 = mycursor.fetchall()
    final.append(myresult2)

    mycursor.execute(s3)
    myresult3 = mycursor.fetchall()
    final.append(myresult3)

    mycursor.execute(s4)
    myresult4 = mycursor.fetchall()
    final.append(myresult4)

    mycursor.execute(s5)
    myresult5 = mycursor.fetchall()
    final.append(myresult5)

    mycursor.execute(s6)
    myresult6 = mycursor.fetchall()
    final.append(myresult6)

    mycursor.execute(s7)
    myresult7 = mycursor.fetchall()
    final.append(myresult7)

    mycursor.execute(s8)
    myresult8 = mycursor.fetchall()
    final.append(myresult8)

    mycursor.execute(s9)
    myresult9 = mycursor.fetchall()
    final.append(myresult9)
    return final


def month_per():
    final = []
    s1 = """SELECT pro_class,QUARTER('2020-03-31'),MONTH('2020-01-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Appliances' AND sto_time <= '2021-03-31' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-03-31'),MONTH('2020-02-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Appliances' AND sto_time <= '2021-03-31' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-03-31'),MONTH('2020-03-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Appliances' AND sto_time <= '2021-03-31' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-06-30'),MONTH('2020-04-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Appliances' AND sto_time <= '2021-06-30' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-06-30'),MONTH('2020-05-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Appliances' AND sto_time <= '2021-06-30' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-06-30'),MONTH('2020-06-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Appliances' AND sto_time <= '2021-06-30' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-09-30'),MONTH('2020-07-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Appliances' AND sto_time <= '2021-06-30' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-09-30'),MONTH('2020-08-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Appliances' AND sto_time <= '2021-06-30' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-09-30'),MONTH('2020-09-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Appliances' AND sto_time <= '2021-09-30' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-12-31'),MONTH('2020-10-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Appliances' AND sto_time <= '2021-12-31' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-12-31'),MONTH('2020-11-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Appliances' AND sto_time <= '2021-12-31' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-12-31'),MONTH('2020-12-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Appliances' AND sto_time <= '2021-12-31' GROUP BY pro_class,s_cost;
            """
    s2 = """SELECT pro_class,QUARTER('2020-03-31'),MONTH('2020-01-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Books' AND sto_time <= '2021-03-31' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-03-31'),MONTH('2020-02-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Books' AND sto_time <= '2021-03-31' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-03-31'),MONTH('2020-03-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Books' AND sto_time <= '2021-03-31' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-06-30'),MONTH('2020-04-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Books' AND sto_time <= '2021-06-30' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-06-30'),MONTH('2020-05-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Books' AND sto_time <= '2021-06-30' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-06-30'),MONTH('2020-06-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Books' AND sto_time <= '2021-06-30' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-09-30'),MONTH('2020-07-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Books' AND sto_time <= '2021-09-30' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-09-30'),MONTH('2020-08-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Books' AND sto_time <= '2021-09-30' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-09-30'),MONTH('2020-09-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Books' AND sto_time <= '2021-09-30' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-12-31'),MONTH('2020-10-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Books' AND sto_time <= '2021-12-31' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-12-31'),MONTH('2020-11-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Books' AND sto_time <= '2021-12-31' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-12-31'),MONTH('2020-12-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Books' AND sto_time <= '2021-12-31' GROUP BY pro_class,s_cost;
            """
    s3 = """SELECT pro_class,QUARTER('2020-03-31'),MONTH('2020-01-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Clothing' AND sto_time <= '2021-03-31' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-03-31'),MONTH('2020-02-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Clothing' AND sto_time <= '2021-03-31' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-03-31'),MONTH('2020-03-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Clothing' AND sto_time <= '2021-03-31' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-06-30'),MONTH('2020-04-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Clothing' AND sto_time <= '2021-06-30' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-06-30'),MONTH('2020-05-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Clothing' AND sto_time <= '2021-06-30' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-06-30'),MONTH('2020-06-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Clothing' AND sto_time <= '2021-06-30' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-09-30'),MONTH('2020-07-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Clothing' AND sto_time <= '2021-09-30' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-09-30'),MONTH('2020-08-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Clothing' AND sto_time <= '2021-09-30' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-09-30'),MONTH('2020-09-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Clothing' AND sto_time <= '2021-09-30' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-12-31'),MONTH('2020-10-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Clothing' AND sto_time <= '2021-12-31' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-12-31'),MONTH('2020-11-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Clothing' AND sto_time <= '2021-12-31' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-12-31'),MONTH('2020-12-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Clothing' AND sto_time <= '2021-12-31' GROUP BY pro_class,s_cost;
            """
    s4 = """SELECT pro_class,QUARTER('2020-03-31'),MONTH('2020-01-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Daily Necessary' AND sto_time <= '2021-03-31' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-03-31'),MONTH('2020-02-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Daily Necessary' AND sto_time <= '2021-03-31' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-03-31'),MONTH('2020-03-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Daily Necessary' AND sto_time <= '2021-03-31' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-06-30'),MONTH('2020-04-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Daily Necessary' AND sto_time <= '2021-06-30' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-06-30'),MONTH('2020-05-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Daily Necessary' AND sto_time <= '2021-06-30' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-06-30'),MONTH('2020-06-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Daily Necessary' AND sto_time <= '2021-06-30' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-09-30'),MONTH('2020-07-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Daily Necessary' AND sto_time <= '2021-09-30' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-09-30'),MONTH('2020-08-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Daily Necessary' AND sto_time <= '2021-09-30' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-09-30'),MONTH('2020-09-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Daily Necessary' AND sto_time <= '2021-09-30' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-12-31'),MONTH('2020-10-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Daily Necessary' AND sto_time <= '2021-12-31' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-12-31'),MONTH('2020-11-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Daily Necessary' AND sto_time <= '2021-12-31' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-12-31'),MONTH('2020-12-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Daily Necessary' AND sto_time <= '2021-12-31' GROUP BY pro_class,s_cost;
            """
    s5 = """SELECT pro_class,QUARTER('2020-03-31'),MONTH('2020-01-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Digital Production' AND sto_time <= '2021-03-31' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-03-31'),MONTH('2020-02-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Digital Production' AND sto_time <= '2021-03-31' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-03-31'),MONTH('2020-03-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Digital Production' AND sto_time <= '2021-03-31' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-06-30'),MONTH('2020-04-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Digital Production' AND sto_time <= '2021-06-30' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-06-30'),MONTH('2020-05-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Digital Production' AND sto_time <= '2021-06-30' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-06-30'),MONTH('2020-06-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Digital Production' AND sto_time <= '2021-06-30' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-09-30'),MONTH('2020-07-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Digital Production' AND sto_time <= '2021-09-30' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-09-30'),MONTH('2020-08-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Digital Production' AND sto_time <= '2021-09-30' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-09-30'),MONTH('2020-09-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Digital Production' AND sto_time <= '2021-09-30' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-12-31'),MONTH('2020-10-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Digital Production' AND sto_time <= '2021-12-31' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-12-31'),MONTH('2020-11-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Digital Production' AND sto_time <= '2021-12-31' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-12-31'),MONTH('2020-12-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Digital Production' AND sto_time <= '2021-12-31' GROUP BY pro_class,s_cost;
            """
    s6 = """SELECT pro_class,QUARTER('2020-03-31'),MONTH('2020-01-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Fruit' AND sto_time <= '2021-03-31' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-03-31'),MONTH('2020-02-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Fruit' AND sto_time <= '2021-03-31' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-03-31'),MONTH('2020-03-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Fruit' AND sto_time <= '2021-03-31' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-06-30'),MONTH('2020-04-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Fruit' AND sto_time <= '2021-06-30' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-06-30'),MONTH('2020-05-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Fruit' AND sto_time <= '2021-06-30' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-06-30'),MONTH('2020-06-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Fruit' AND sto_time <= '2021-06-30' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-09-30'),MONTH('2020-07-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Fruit' AND sto_time <= '2021-09-30' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-09-30'),MONTH('2020-08-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Fruit' AND sto_time <= '2021-09-30' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-09-30'),MONTH('2020-09-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Fruit' AND sto_time <= '2021-09-30' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-12-31'),MONTH('2020-10-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Fruit' AND sto_time <= '2021-12-31' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-12-31'),MONTH('2020-11-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Fruit' AND sto_time <= '2021-12-31' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-12-31'),MONTH('2020-12-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Fruit' AND sto_time <= '2021-12-31' GROUP BY pro_class,s_cost;
            """
    s7 = """SELECT pro_class,QUARTER('2020-03-31'),MONTH('2020-01-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Furniture' AND sto_time <= '2021-03-31' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-03-31'),MONTH('2020-02-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Furniture' AND sto_time <= '2021-03-31' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-03-31'),MONTH('2020-03-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Furniture' AND sto_time <= '2021-03-31' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-06-30'),MONTH('2020-04-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Furniture' AND sto_time <= '2021-06-30' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-06-30'),MONTH('2020-05-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Furniture' AND sto_time <= '2021-06-30' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-06-30'),MONTH('2020-06-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Furniture' AND sto_time <= '2021-06-30' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-09-30'),MONTH('2020-07-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Furniture' AND sto_time <= '2021-09-30' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-09-30'),MONTH('2020-08-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Furniture' AND sto_time <= '2021-09-30' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-09-30'),MONTH('2020-09-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Furniture' AND sto_time <= '2021-09-30' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-12-31'),MONTH('2020-10-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Furniture' AND sto_time <= '2021-12-31' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-12-31'),MONTH('2020-11-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Furniture' AND sto_time <= '2021-12-31' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-12-31'),MONTH('2020-12-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Furniture' AND sto_time <= '2021-12-31' GROUP BY pro_class,s_cost;
            """
    s8 = """SELECT pro_class,QUARTER('2020-03-31'),MONTH('2020-01-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Medicine' AND sto_time <= '2021-03-31' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-03-31'),MONTH('2020-02-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Medicine' AND sto_time <= '2021-03-31' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-03-31'),MONTH('2020-03-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Medicine' AND sto_time <= '2021-03-31' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-06-30'),MONTH('2020-04-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Medicine' AND sto_time <= '2021-06-30' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-06-30'),MONTH('2020-05-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Medicine' AND sto_time <= '2021-06-30' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-06-30'),MONTH('2020-06-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Medicine' AND sto_time <= '2021-06-30' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-09-30'),MONTH('2020-07-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Medicine' AND sto_time <= '2021-09-30' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-09-30'),MONTH('2020-08-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Medicine' AND sto_time <= '2021-09-30' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-09-30'),MONTH('2020-09-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Medicine' AND sto_time <= '2021-09-30' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-12-31'),MONTH('2020-10-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Medicine' AND sto_time <= '2021-12-31' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-12-31'),MONTH('2020-11-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Medicine' AND sto_time <= '2021-12-31' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-12-31'),MONTH('2020-12-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Medicine' AND sto_time <= '2021-12-31' GROUP BY pro_class,s_cost;
            """
    s9 = """SELECT pro_class,QUARTER('2020-03-31'),MONTH('2020-01-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Seafood' AND sto_time <= '2021-03-31' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-03-31'),MONTH('2020-02-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Seafood' AND sto_time <= '2021-03-31' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-03-31'),MONTH('2020-03-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Seafood' AND sto_time <= '2021-03-31' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-06-30'),MONTH('2020-04-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Seafood' AND sto_time <= '2021-06-30' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-06-30'),MONTH('2020-05-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Seafood' AND sto_time <= '2021-06-30' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-06-30'),MONTH('2020-06-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Seafood' AND sto_time <= '2021-06-30' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-09-30'),MONTH('2020-07-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Seafood' AND sto_time <= '2021-09-30' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-09-30'),MONTH('2020-08-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Seafood' AND sto_time <= '2021-09-30' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-09-30'),MONTH('2020-09-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Seafood' AND sto_time <= '2021-09-30' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-12-31'),MONTH('2020-10-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Seafood' AND sto_time <= '2021-12-31' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-12-31'),MONTH('2020-11-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Seafood' AND sto_time <= '2021-12-31' GROUP BY pro_class,s_cost UNION ALL
            SELECT pro_class,QUARTER('2020-12-31'),MONTH('2020-12-01'),CONCAT((1/3)*100,'%') FROM products_inventory join class_region ON pro_class = c_name WHERE pro_class = 'Seafood' AND sto_time <= '2021-12-31' GROUP BY pro_class,s_cost;
            """

    mycursor.execute(s1)
    myresult1 = mycursor.fetchall()
    final.append(myresult1)

    mycursor.execute(s2)
    myresult2 = mycursor.fetchall()
    final.append(myresult2)

    mycursor.execute(s3)
    myresult3 = mycursor.fetchall()
    final.append(myresult3)

    mycursor.execute(s4)
    myresult4 = mycursor.fetchall()
    final.append(myresult4)

    mycursor.execute(s5)
    myresult5 = mycursor.fetchall()
    final.append(myresult5)

    mycursor.execute(s6)
    myresult6 = mycursor.fetchall()
    final.append(myresult6)

    mycursor.execute(s7)
    myresult7 = mycursor.fetchall()
    final.append(myresult7)

    mycursor.execute(s8)
    myresult8 = mycursor.fetchall()
    final.append(myresult8)

    mycursor.execute(s9)
    myresult9 = mycursor.fetchall()
    final.append(myresult9)
    return final


@app.route('/')
def login_page():
    return render_template("Login.html")


@app.route('/login', methods=["GET", "POST"])
def login_auth():
    username = request.form.get('emp_username')
    password = request.form.get('emp_password')
    # userid = EmpUser.query.filter(EmpUser.emp_username == username).first().emp_id
    if request.method == 'POST':
        session['username'] = username
        realuser = EmpUser.query.filter(EmpUser.emp_username == username).first()
    if realuser is not None:
        if realuser.emp_level == 3:
            session['username_level'] = 'manager'
        elif realuser.emp_level <= 2:
            session['username_level'] = 'worker'
    else:
        return redirect(url_for('login_failure'))

    if realuser is not None:
        if password == realuser.emp_password:
            # new_users = EmpLoginRecord(emp_id = userid)
            # s.add(new_users)
            # s.commit()
            # s.close()
            return redirect(url_for('login_success'))
        else:
            return redirect(url_for('login_failure'))
    else:
        return redirect(url_for('login_failure'))

    return render_template('Login.html')


@app.route('/login_successful')
def login_success():
    if session['username_level'] == 'manager':
        return redirect(url_for('main_page'))
    if session['username_level'] == 'worker':
        return redirect(url_for('main_page_worker'))


@app.route('/login_failed')
def login_failure():
    return render_template('Login_Failed.html')


@app.route('/logout')
def logout():
    del session['username'], session['username_level']
    # username = session['username']
    # userid = EmpUser.query.filter(EmpUser.emp_username == username).first().emp_id
    # deuser =  EmpLoginRecord.query.filter(EmpLoginRecord.emp_id == userid).one()
    # s.delete(deuser)
    # s.commit()
    # s.close())
    return redirect(url_for('login_page'))


@app.route('/main_page')
def main_page():
    lst = db.session.query(ProductsInventory).filter(ProductsInventory.pro_city == 'Shanghai').all()
    if session.get('in_city') is None:
        session['in_city'] = 'Shanghai'
        return render_template('Main_Page_manager.html', lst=lst)
    else:
        alt = db.session.query(ProductsInventory).filter(ProductsInventory.pro_city == session['in_city']).all()
        print(lst)
        return render_template('Main_Page_manager.html', lst=alt)


@app.route('/main_page_switching', methods=["GET", "POST"])
def main_page_switch():
    if request.method == 'POST':
        session['in_city'] = request.form.get('data')

        return redirect(url_for('main_page'))


@app.route('/main_page_worker')
def main_page_worker():
    lst = db.session.query(ProductsInventory).all()
    return render_template('Main_Page_worker.html', lst=lst)


@app.route('/add', methods=["GET", "POST"])
def main_create():
    name = request.form.get('item_name')
    region = request.form.get('item_category')
    region_number = request.form.get('item_location')
    amount = request.form.get('item_amount')
    charge = request.form.get('item_pic')
    remark = request.form.get('item_remarks')
    storage_time = request.form.get('item_stored_time')

    item = db.session.query(ProductsInventory).filter(ProductsInventory.pro_name == name).first()

    if item is not None:
        item.pro_amount += int(amount)
        db.session.commit()
        db.session.close()
        return redirect(url_for('main_page'))
    else:
        category = db.session.query(ClassRegion).filter(ClassRegion.r_name == region).first()
        new_pro = ProductsInventory \
            (pro_name=name, pro_class=category.c_name, pro_charge=charge, pro_region=region, re_section=region_number,
             pro_amount=amount, pro_remark=remark, sto_time=storage_time, pro_city=session['in_city'])
        db.session.add(new_pro)
        db.session.commit()
        db.session.close()

        return redirect(url_for('main_page'))

    return render_template("Main_Page_manager.html")


@app.route('/search', methods=["GET", "POST"])
def main_search():
    global item
    if request.method == 'POST':
        search_str = request.form.get("search_database")
        item = db.session.query(ProductsInventory).filter(ProductsInventory.pro_name == search_str).first()
    if item is not None:
        return render_template("Main_Page_manager.html", sgl=item)
    else:
        return redirect(url_for('search_failure'))


@app.route('/search_failure')
def search_failure():
    return render_template('Search_Failure.html')


@app.route('/delete', methods=["POST"])
def main_delete():
    if request.method == 'POST':
        delete_list = json.loads(request.form.get('data'))
        print(delete_list['deletion'])

        if delete_list['deletion'] is not None:
            for i in delete_list['deletion']:
                delete_product = db.session.query(ProductsInventory).filter(ProductsInventory.pro_name == i).first()
                db.session.delete(delete_product)
                db.session.commit()
            return redirect(url_for('main_page'))
        else:
            return redirect(url_for('main_page'))


@app.route('/modify_preparation', methods=["POST"])
def modify_prepare():
    global original_name
    original_name = json.loads(request.form.get('data'))
    # print(original_name['modify_item'])
    return redirect(url_for("main_page"))


@app.route('/modify', methods=["GET", "POST"])
def main_modify():
    print(original_name['modify_item'])

    item = db.session.query(ProductsInventory).filter(
        ProductsInventory.pro_name == original_name['modify_item']).first()

    print(item.pro_charge)

    if request.method == 'POST':

        modify_name = request.form.get('modify_item_name')
        modify_category = request.form.get('modify_item_category')
        modify_pic = request.form.get('modify_item_pic')
        modify_region_number = request.form.get('modify_item_location')
        modify_amount = request.form.get('modify_item_amount')
        modify_remarks = request.form.get('modify_item_remarks')
        modify_storage_time = request.form.get('modify_item_stored_time')

        print(modify_name, modify_category)
        if modify_name == 'null':
            item.pro_name = item.pro_name
        else:
            item.pro_name = modify_name

        if modify_category == 'null':
            item.pro_class = item.pro_class
        else:
            item.pro_class = db.session.query(ClassRegion).filter(ClassRegion.r_name == modify_category).first().c_name
            item.pro_region = modify_category

        if modify_pic == 'null':
            item.pro_charge = item.pro_charge
        else:
            item.pro_charge = modify_pic

        if modify_region_number == 'null':
            item.re_section = 1
        else:
            pass

        if modify_remarks == 'null':
            item.pro_remark = item.pro_remark
        else:
            item.pro_remark = modify_remarks

        if modify_amount == 'null':
            item.pro_amount = item.pro_amount
        else:
            item.pro_amount = modify_amount
        db.session.commit()
        db.session.close()
    return redirect(url_for('main_page'))


@app.route('/financial_budget', methods=["POST"])
def collect_budget():
    if request.method == 'POST':
        session['budget_settings'] = []
        session['budget_settings'].append(total_budget=request.form.get('total_budget'))
        session['budget_settings'].append(a_budget=request.form.get('a_budget'))
        session['budget_settings'].append(b_budget=request.form.get('b_budget'))
        session['budget_settings'].append(c_budget=request.form.get('c_budget'))
        session['budget_settings'].append(d_budget=request.form.get('d_budget'))
        session['budget_settings'].append(e_budget=request.form.get('e_budget'))
        session['budget_settings'].append(f_budget=request.form.get('f_budget'))
        session['budget_settings'].append(g_budget=request.form.get('g_budget'))
        session['budget_settings'].append(h_budget=request.form.get('h_budget'))
        session['budget_settings'].append(i_budget=request.form.get('i_budget'))


@app.route('/financial_time')
def financial_time():
    return render_template('Financial_time.html')


@app.route('/financial_category')
def financial_category():
    return render_template('Financial_category2.html')


@app.route('/financial')
def main_financial():
    return render_template('Financial.html')


@app.route('/fixed_time_budget', methods=["POST"])
def get_fixed_time_budget():
    if request.method == 'POST':
        session['fst_quarter'] = []

        session['fst_quarter'].append(int(request.form.get('Fruit_budget_1')))
        session['fst_quarter'].append(int(request.form.get('Seafood_budget_1')))
        session['fst_quarter'].append(int(request.form.get('Digital_budget_1')))
        session['fst_quarter'].append(int(request.form.get('Clothing_budget_1')))
        session['fst_quarter'].append(int(request.form.get('Furniture_budget_1')))
        session['fst_quarter'].append(int(request.form.get('Books_budget_1')))
        session['fst_quarter'].append(int(request.form.get('Appliances_budget_1')))
        session['fst_quarter'].append(int(request.form.get('Necessities_budget_1')))
        session['fst_quarter'].append(int(request.form.get('Medicine_budget_1')))

        total_budget = 0

        db.session.query(ClassRegion).filter(ClassRegion.r_name == 'A').first().r_budget = session['fst_quarter'][0]
        db.session.query(ClassRegion).filter(ClassRegion.r_name == 'B').first().r_budget = session['fst_quarter'][1]
        db.session.query(ClassRegion).filter(ClassRegion.r_name == 'C').first().r_budget = session['fst_quarter'][2]
        db.session.query(ClassRegion).filter(ClassRegion.r_name == 'D').first().r_budget = session['fst_quarter'][3]
        db.session.query(ClassRegion).filter(ClassRegion.r_name == 'E').first().r_budget = session['fst_quarter'][4]
        db.session.query(ClassRegion).filter(ClassRegion.r_name == 'F').first().r_budget = session['fst_quarter'][5]
        db.session.query(ClassRegion).filter(ClassRegion.r_name == 'G').first().r_budget = session['fst_quarter'][6]
        db.session.query(ClassRegion).filter(ClassRegion.r_name == 'H').first().r_budget = session['fst_quarter'][7]
        db.session.query(ClassRegion).filter(ClassRegion.r_name == 'I').first().r_budget = session['fst_quarter'][8]
        db.session.commit()
        db.session.close()

        for i in range(0, len(session['fst_quarter'])):
            total_budget = session['fst_quarter'][i] + total_budget

        session['total_budget'] = total_budget
    return redirect(url_for('main_financial'))


"""@app.route('/financial_time_comparison')
def fixed_category():"""


@app.route('/financial_category_comparison', methods=["POST"])
def fixed_time():
    if request.method == 'POST':
        s1 = "SELECT pro_class,CONVERT(SUM(pro_amount)*s_cost*90,UNSIGNED),r_budget,CONCAT(round(SUM(pro_amount)*s_cost*90/r_budget*100),'%')  from products_inventory join class_region ON pro_class = c_name WHERE sto_time <= '2021-03-31' GROUP BY pro_class;"
        s2 = "SELECT pro_class,CONVERT(SUM(pro_amount)*s_cost*90,UNSIGNED),r_budget,CONCAT(round(SUM(pro_amount)*s_cost*90/r_budget*100),'%')  from products_inventory join class_region ON pro_class = c_name WHERE sto_time <= '2021-06-30' GROUP BY pro_class;"
        s3 = "SELECT pro_class,CONVERT(SUM(pro_amount)*s_cost*90,UNSIGNED),r_budget,CONCAT(round(SUM(pro_amount)*s_cost*90/r_budget*100),'%')  from products_inventory join class_region ON pro_class = c_name WHERE sto_time <= '2021-09-30' GROUP BY pro_class;"
        s4 = "SELECT pro_class,CONVERT(SUM(pro_amount)*s_cost*90,UNSIGNED),r_budget,CONCAT(round(SUM(pro_amount)*s_cost*90/r_budget*100),'%')  from products_inventory join class_region ON pro_class = c_name WHERE sto_time <= '2021-12-31' GROUP BY pro_class;"
        total = []
        mycursor.execute(s1)
        myresult1 = mycursor.fetchall()
        myresult1.insert(0, 1)
        total.append(myresult1)

        mycursor.execute(s2)
        myresult2 = mycursor.fetchall()
        myresult2.insert(0, 2)
        total.append(myresult2)

        mycursor.execute(s3)
        myresult3 = mycursor.fetchall()
        myresult3.insert(0, 3)
        total.append(myresult3)

        mycursor.execute(s4)
        myresult4 = mycursor.fetchall()
        myresult4.insert(0, 4)
        total.append(myresult4)
        print(total)
        return jsonify(total)


@app.route('/visualization')
def visuals():
    return render_template('Visualization.html')


@app.route('/communication')
def communication():
    if session['username_level'] == 'manager':
        lst = db.session.query(ProductsInventory).filter(ProductsInventory.pro_city == session['in_city']).all()
        return render_template('Communication_manager.html', lst=lst)
    if session['username_level'] == 'worker':
        lst = db.session.query(ProductsInventory).filter(ProductsInventory.pro_city == session['in_city']).all()
        return render_template('Communication_worker.html', lst=lst)


'''@app.route('/communication_manager_main',methods=["POST"])
def communication_manger_main():
    if request.method == 'POST':



@app.route('/')'''


@app.route('/3Dmapping')
def three_d_map():
    return render_template('3DProject.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=18080, debug=True)
