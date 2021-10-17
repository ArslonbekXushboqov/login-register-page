import sqlite3 as sql

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

s = input("Login/Register (l/r)? ")
if s=='r':
    try:
        fname = str(input("Ismingizni kiriting: "))
        lname = str(input("Familiyangizni kiriting: "))
        age = int(input("Yoshingizni kiriting: "))
        login = input("Login yarating (minimal 5 ta belgi): ")
        passw = input("Parol yarating (minimal 8 ta belgi): ")
        
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
    login = input("Loginni kiriting: ")

    con = sql.connect(db)
    cur = con.cursor()
    cur.execute("SELECT login FROM user WHERE login = ?",(login,))
    res = cur.fetchone()
    if res is not None:
        passw = input("Parolni kiriting: ")

        cur.execute("SELECT passw FROM user WHERE login = ?",(login,))
        p = list(cur.fetchone())
        if p[0] == passw:
            cur.execute("SELECT fname,lname,age FROM user WHERE passw = ?",(passw,))
            res = cur.fetchall()
            data = list(res[0])
            ism = data[0]
            fam = data[1]
            yosh = data[2]
            m = input("""\n      Ma\'lumotlaringiz [1] Sozlamalar [2] Akkauntni o\'chirish [3] \n                            Chiqish [exit]\n            Tanlang: """)
            if m=='1':
                print(f"Ismingiz: {ism}\nFamiliyangiz: {fam}\nYoshingiz: {yosh} da.")
            elif m=='2':
                s = input("\n      Ism o\'zgartirish [1] Familiyani o\'zgartirish [2] Parol o\'zgartirish [3] \n                                Orqaga [orqaga]\n            Tanlang: ")
                if s=='1':
                    i = str(input("Ism kiriting: "))

                    cur.execute("UPDATE user SET fname = ? WHERE fname = ?", (i,ism,))
                    con.commit()
                    print(f"Ism [{ism}] dan [{i}] ga o\'zgartirildi.")
                elif s=='2':
                    f = str(input("Familiya kiriting: "))

                    cur.execute("UPDATE user SET lname = ? WHERE lname = ?", (f,fam,))
                    con.commit()
                    print(f"Familiya [{fam}] dan [{f}] ga o\'zgartirildi.")
                elif s=='3':
                    h = input("Hozirgi parolni kiriting: ")
                    if h==p[0]:
                        y = input("Yangi parolni kiriting: ")

                        con = sql.connect(db)
                        cur = con.cursor()
                        cur.execute("UPDATE user SET passw = ? WHERE passw = ?",(y, p[0],))
                        con.commit()
                        print(f"Parol [{h}] dan [{y}] ga o\'zgartirildi.")
                    else:
                        print("Parol xato")
            elif m=='3':
             l = input("Akkauntingini haqiqatdan o\'chirmoqchimisiz(y/n)? ")
             if l == 'y':
                 con = sql.connect(db)
                 cur = con.cursor()
                 cur.execute("""DELETE FROM user WHERE login = ?""", (login,))
                 con.commit()
                 print("Muvaffaqiyatli o\'chirildi.")
            else:
                print("Bekor qilindi.")
                
        else:
            print("Parol no\'to\'g\'ri!")
    else:
        print("Bunday login bazada mavjud emas")
        
