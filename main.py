import json
import sqlite3

import qrcode
from flask import Flask, render_template, request, redirect, send_file

with open('settings.json', 'r') as config_file:
    config = json.load(config_file)

db_path = config["db_path"]
Ticket_Name = config["Ticket_Name"]
max_ppl = config["max_ppl"]
qr_file_path = config["qr_file_path"]
input_form_msg = config["input_form_msg"]
no_name = config["no_name"]
no_ppl = config["no_ppl"]
qr_msg= config["qr_msg"]
app = Flask(__name__, static_folder='./templates')


@app.route("/")
def index():
    return render_template("index.html",
                           max_ppl=max_ppl, input_form_msg=input_form_msg)


@app.route("/api_new_data", methods=["POST"])
def api_new_data():
    data = request.form
    name = data.get("name")
    if name == "":
        name = no_name
    ppl = data.get("ppl")
    if ppl == 0 or ppl == "":
        ppl = no_ppl
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM my_table ORDER BY id DESC LIMIT 1")
    id = cursor.fetchall()
    conn.close()
    if id == []:
        ticket_id = Ticket_Name + "1"
    else:
        tk_num = id[0][0] + 1
        tk_num_str = str(tk_num)  # 数値を文字列に変換
        ticket_id = Ticket_Name + tk_num_str  # 文字列の結合

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO my_table (name, ppl, ticket_id) VALUES (?, ?, ?)", (name, ppl, ticket_id))
    conn.commit()  # 変更をコミット
    conn.close()

    qr = qrcode.QRCode(
        version=1,  # QRコードのバージョン
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # 誤り訂正レベル
        box_size=10,  # ボックスのサイズ
        border=4,  # 境界のサイズ
    )
    qr.add_data(ticket_id)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(f"{qr_file_path}/{ticket_id}.png")
    return redirect("/preview/"+ticket_id)


@app.route("/preview/<url>")
def preview(url):
    img_path = url + "/dw"
    ticket_name = "チケット名:"+url
    return render_template("preview.html", qr_path=img_path,
                           download_path=img_path, ticket_name=ticket_name)


@app.route("/preview/<url>/dw")
def preview_dw(url):
    image_path = qr_file_path + "/" + url + ".png"
    return send_file(image_path, mimetype="image/png", as_attachment=True)

@app.route("/welcome")
def welcome():
    return render_template("welcome.html",qr_msg=qr_msg)
if __name__ == '__main__':
    app.run(debug=True)
