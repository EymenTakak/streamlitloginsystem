import streamlit as st
import sqlite3 as sq
import pandas as pd
import json
import pyqrcode as py
from urllib.request import urlopen

tab1, tab2 = st.tabs(["Log On", "Sign Up"])

conn=sq.connect("login.db")
c=conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS product(productname TEXT, productimage TEXT, productbrand TEXT, productprice REAL, productsource TEXT)")
conn.commit()



with tab2:
    c.execute("CREATE TABLE IF NOT EXISTS login(isim TEXT, klcad TEXT ,mail TEXT ,sifre text)")
    conn.commit()

    def addworker(isim,klcad,mail,sifre):
      c.execute("SELECT*FROM login WHERE klcad=?",(klcad,))
      a=c.fetchall()
      c.execute("SELECT*FROM login WHERE mail=?", (mail,))
      b=c.fetchall()
      if (len(a)==0) and (len(b)==0):
        c.execute("INSERT INTO login VALUES(?,?,?,?)",(isim,klcad,mail,sifre))
        conn.commit()
        mesaj = "Register Completed."
      else:
        mesaj = "Email or Nickname is already taken"
      st.warning(mesaj)

    with st.form("wordkerekle",clear_on_submit=True):
        isim = st.text_input("Name: ",max_chars=15,)
        klcad = st.text_input("Username: ",max_chars=10, autocomplete="nickname")
        mail = st.text_input("Mail: ", autocomplete="email")
        sifre = st.text_input("Password: ", max_chars=18, type="password",autocomplete="password")


        sumbitted = st.form_submit_button("Sign Up")

        if sumbitted:
            addworker(isim,klcad,mail,sifre)



with tab1:
    def checklog(klcad,sifre):
        c.execute(f"SELECT * FROM login WHERE klcad='{klcad}' AND sifre='{sifre}';")
        a = c.fetchone()
        if not a:
            st.warning("Username Or Password is Wrong")
        elif a:
            st.warning("login successful...")
            tab3,tab4,tab5,tab6 = st.tabs(["Custom Products","Manage Person","JSON To Qr","Manage Work Times"])

            with tab3:

                def addproduct(nm, img, br, pr, sr):
                    c.execute("INSERT INTO product VALUES(?,?,?,?,?)", (nm, img, br, pr, sr))
                    conn.commit()
                    mesaj = "ADDED"
                    return st.warning(mesaj)


                with st.form("custom"):
                    name = st.text_input("Product Name: ")
                    image = st.text_input("Product Image Link: ")
                    brand = st.text_input("Product Brand: ")
                    price = st.number_input("Product Price: ")
                    source = st.text_input("Product Source: ")

                    succ = st.form_submit_button("Add")

                if succ:
                    addproduct(name,image,brand,price,source)

                c.execute("SELECT * FROM product")
                u = c.fetchall()
                v = pd.DataFrame(u)
                st.dataframe(v)

            with tab5:

                js = st.text_input("Json Api Link", "")
                dictt = st.text_input("Dict Value", "Write Your Json Dict Value")
                z = st.number_input("Qr Scale: recommended=8", )

                def createqr():
                    with urlopen(js) as response:
                        source = response.read()
                        veri = json.loads(source)
                    t = 0
                    for res in veri:
                        t += 1
                        x = res[dictt]
                        y = py.create(x)
                        y.svg(f"qr{t}.svg", scale=z)

                if st.button("Create"):
                    createqr()
                    st.warning("Wait a few minutes...")





    with st.form("deneme",clear_on_submit=True):
        kullanici = st.text_input("Username: ")
        sifre = st.text_input("Password: ", type="password")

        login = st.form_submit_button("Log On")

    if login:
        checklog(kullanici,sifre)

