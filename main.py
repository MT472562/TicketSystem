import json
import os
import sqlite3

import qrcode
from flask import Flask, render_template, request, redirect, send_file, jsonify

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

@app.errorhandler(404)
def error_404(error):
    return render_template("errors.html", title="404 Not Found",
                           error_id="404", error_msg="The page you were looking for could not be found.",
                           error_detail="We couldn't locate the page you were looking for, and it's possible that the page has been removed. Please feel free to get in touch with our support team for further assistance.",
                           error_msg_jp="お探しのページが見つかりませんでした")

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
    cursor.execute("INSERT INTO my_table (name, ppl, ticket_id,status) VALUES (?, ?, ?,?)",
                   (name, ppl, ticket_id, "登録済み"))
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
    file_path = qr_file_path + "/" + url + ".png"
    img_path = url + "/dw"
    ticket_name = "チケット名:"+url
    if os.path.exists(file_path):
        return render_template("preview.html", qr_path=img_path,
                               download_path=img_path, ticket_name=ticket_name)
    else:
        return render_template("errors.html", title="404 Not Found",
                               error_id="404", error_msg="The ticket does not exist.",
                               error_detail="This ticket does not exist. If the ticket ID is correct and you are seeing this page, please contact customer support.",
                               error_msg_jp="指定されたチケットの存在が確認できませんでした")


@app.route("/preview/<url>/dw")
def preview_dw(url):
    image_path = qr_file_path + "/" + url + ".png"
    return send_file(image_path, mimetype="image/png", as_attachment=True)

@app.route("/welcome")
def welcome():
    return render_template("welcome.html",qr_msg=qr_msg)


@app.route("/status_update", methods=["POST"])
def status_update():
    post_data = request.json
    post_status = post_data["status"]
    ticket_id = post_data["key"]
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM my_table WHERE ticket_id = ?", (ticket_id,))
    result = cursor.fetchall()
    if not result:
        return jsonify({"status": 404, "msg": "チケットが見つかりませんでした","data":""})
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    status_mapping = {
        "入場": ("入場中", "が入場しました"),
        "一時退場": ("一時退場中", "が一時退場しました"),
        "退場": ("退場済み", "が退場しました"),
    }
    default_status = ("", "")
    status, msg_suffix = status_mapping.get(post_status, default_status)
    msg = f"{ticket_id} {msg_suffix}"
    cursor.execute("UPDATE my_table SET status = ? WHERE ticket_id = ?", (status, ticket_id))

    conn.commit()
    conn.close()
    return jsonify({"status": 200, "msg": msg,"data":result})

@app.route("/view")
def view():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM my_table")
    result = cursor.fetchall()
    conn.close()
    return render_template("view.html",table_data=result )
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7400)
