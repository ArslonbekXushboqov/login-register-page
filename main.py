import sqlite3 as sql
from os import system

db = "baza.db"

with sql.connect(db) as con:
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS user(
        login VARCHAR,
        passw VARCHAR,
        fname TEXT,
        lname TEXT,
        age INTEGER
    )""")
    con.commit()
system("cls")
print("                     Login-Register Page By Arslonbek                    \n")
s = input("Login/Register (l/r)? ")
if s=='r':
    try:
        system("cls")
        fname = str(input("Ismingizni kiriting: "))
        system("cls")
        lname = str(input("Familiyangizni kiriting: "))
        system("cls")
        age = int(input("Yoshingizni kiriting: "))
        system("cls")
        login = input("Login yarating (minimal 5 ta belgi): ")
        system("cls")
        passw = input("Parol yarating (minimal 8 ta belgi): ")
        system("cls")
        if len(login)>=5 and len(passw)>=8:
            con = sql.connect(db)
            cur = con.cursor()
            cur.execute("SELECT login FROM user WHERE login = ?",(login,))
            if cur.fetchone() is not None:
                print("Ushbu login bazada mavjud!")
            else:
                cur.execute("INSERT INTO user(fname,lname,age,login,passw) VALUES(?,?,?,?,?)", (fname,lname,age,login,passw,))
                con.commit()
                print("Muvaffaqiyatli yaratildi!")
        else:
            print("Parol yoki login no\'to\'g\'ri kiritildi.")
    except Exception as ex:
        print(f"Xatolik: {ex}")
elif s=='l':
    system("cls")
    login = input("Loginni kiriting: ")

    con = sql.connect(db)
    cur = con.cursor()
    cur.execute("SELECT login FROM user WHERE login = ?",(login,))
    res = cur.fetchone()
    if res is not None:
        system("cls")
        passw = input("Parolni kiriting: ")

        cur.execute("SELECT passw FROM user WHERE login = ?",(login,))
        p = list(cur.fetchone())
        if p[0] == passw:
            system("cls")
            cur.execute("SELECT fname,lname,age FROM user WHERE passw = ?",(passw,))
            res = cur.fetchall()
            data = list(res[0])
            ism = data[0]
            fam = data[1]
            yosh = data[2]
            m = input("""\n      Ma\'lumotlaringiz [1] Sozlamalar [2] Akkauntni o\'chirish [3] \n                            Chiqish [exit]\n            Tanlang: """)
            if m=='1':
                system("cls")
                print(f"Ismingiz: {ism}\nFamiliyangiz: {fam}\nYoshingiz: {yosh} da.")
            elif m=='2':
                system("cls")
                s = input("\n      Ism o\'zgartirish [1] Familiyani o\'zgartirish [2] Parol o\'zgartirish [3] \n                                Orqaga [orqaga]\n            Tanlang: ")
                if s=='1':
                    system("cls")
                    i = str(input("Ism kiriting: "))

                    cur.execute("UPDATE user SET fname = ? WHERE fname = ?", (i,ism,))
                    con.commit()
                    system("cls")
                    print(f"Ism [{ism}] dan [{i}] ga o\'zgartirildi.")
                elif s=='2':
                    system("cls")
                    f = str(input("Familiya kiriting: "))

                    cur.execute("UPDATE user SET lname = ? WHERE lname = ?", (f,fam,))
                    con.commit()
                    system("cls")
                    print(f"Familiya [{fam}] dan [{f}] ga o\'zgartirildi.")
                elif s=='3':
                    system("cls")
                    h = input("Hozirgi parolni kiriting: ")
                    if h==p[0]:
                        system("cls")
                        y = input("Yangi parolni kiriting: ")

                        con = sql.connect(db)
                        cur = con.cursor()
                        cur.execute("UPDATE user SET passw = ? WHERE passw = ?",(y, p[0],))
                        con.commit()
                        system("cls")
                        print(f"Parol [{h}] dan [{y}] ga o\'zgartirildi.")
                    else:
                        print("Parol xato")
            elif m=='3':
             system("cls")
             l = input("Akkauntingini haqiqatdan o\'chirmoqchimisiz(y/n)? ")
             if l == 'y':
                 con = sql.connect(db)
                 cur = con.cursor()
                 cur.execute("""DELETE FROM user WHERE login = ?""", (login,))
                 con.commit()
                 system("cls")
                 print("Muvaffaqiyatli o\'chirildi.")
            else:
                system("cls")
                print("Bekor qilindi.")
                
        else:
            print("Parol no\'to\'g\'ri!")
    else:
        print("Bunday login bazada mavjud emas")
        
