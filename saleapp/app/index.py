import math

from flask import render_template, request, redirect, jsonify, send_file, g, session
import dao
from app import app, login
from flask_login import login_user, logout_user

import pandas as pd
from io import BytesIO
@app.route("/", methods=['get', 'post'])
def index():
    if request.method.__eq__('POST'):
        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        address = request.form.get('address')
        time = request.form.get('time')
        note = request.form.get('note')
        date = request.form.get('date')
        a = dao.create_appointment(name = name, phone=phone, email=email, address=address, time = time, note = note,date_examination=date)
        return redirect(request.referrer or '/')
    else:
        time_frames = dao.get_list_time_frame()
        return render_template('index.html',time_frames=time_frames)

   # return render_template('index.html', categories = cates, products = prods, page = math.ceil(total/page_size))

@app.route("/login", methods=['get', 'post'])
def login_procee():
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        u = dao.auth_user(username, password)
        if u:
            print(u)
            login_user(u)
            return redirect('/')



    return render_template('login.html')



@login.user_loader
def get_user(user_id):
    return dao.get_user_by_id(user_id)

@app.route("/logout")
def logout_procees():
    logout_user()
    return redirect('/login')



@app.route("/createList", methods =['get','post'])
def create_list_procee():
    if request.method.__eq__('POST'):
        appointment_date = request.form.get('appointment_date')

        record = dao.get_list_patient2(appointment_date)
        print(record)
        return render_template('list.html', records = record)

    return render_template('list.html')

@app.route("/abc", methods=['get', 'post'])
def medi():
    if request.method.__eq__('POST'):
        a = request.form.get('ids')
        print(a)
        return render_template('medicineb.html')
    return render_template('medicineb.html')



@app.route("/login-admin",methods=['post'])
def login_admin_procees():
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        u = dao.auth_user(username, password)
        if u:
            login_user(u)
            return redirect('/admin')
        return redirect('/admin')

@app.route("/api/timeframe", methods=['GET'])
def timeframe_procee():

    time_frames = dao.get_list_time_frame()
    data = []
    for time_frame in time_frames:
        data.append({'time': time_frame.time})

    print(time_frames)
    # Trả về dữ liệu dưới dạng JSON
    return jsonify(data)  # Đảm bảo trả về đối tượng jsonify để Flask trả về response JSON

@app.route("/export_excel")
def export_excel_procee():
    # data = [
    #     {'examination_id': 5, 'patient_name': 'aa', 'patient_id': 5, 'time': '3:00', 'examination_date': '2024-12-20'},
    #     {'examination_id': 5, 'patient_name': 'aa', 'patient_id': 5, 'time': '3:00', 'examination_date': '2024-12-20'}
    # ]
    data = session.get('result_data', None)
    df = pd.DataFrame(data)

    # Sử dụng BytesIO để lưu tạm file Excel trong bộ nhớ (không ghi vào disk)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Examination Data')

    # Đưa con trỏ về đầu file
    output.seek(0)

    # Gửi file Excel về phía người dùng
    return send_file(output, as_attachment=True, download_name="examination_data.xlsx",
                     mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

if __name__ == '__main__':
    from app import admin
    app.run(debug=True)
