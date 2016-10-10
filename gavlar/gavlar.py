from flask import Flask, request, jsonify, render_template

from pyexcel_ods import get_data

app=Flask(__name__)

# https://127.0.0.1/read
@app.route("/read", methods=['GET'])
def read_records():
    ods_data = get_data("../input/en/sample.ods")
    ret_data = {}

    for sheet in ods_data:

        if (sheet != 'start') and (sheet != 'end'):

            ret_data[sheet] = []
            question = {}

            for row_no, row in enumerate(ods_data[sheet]):

                if (row_no > 0) and (len(row) > 1):

                    if row[0] != '':
                        question['smart_key'] = row[0]
                        question['smart_key_type'] = row[1]
                        question['question'] = row[2]
                        answer = []

                    if len(row) == 6:
                        answer.append({
                          "answer_number": row[3], "answer_text": row[5], "smart_value_key": row[4]
                        })

                    if row[0] != '':
                        question['answers'] = answer
                        ret_data[sheet].append(question)
                        question = { 'answers': [] }

    return jsonify(ret_data)

# https://127.0.0.1/gps?phone=12345678
@app.route("/gps", methods=['GET'])
def gps():

    phone = request.values.get('phone')

    return render_template('gps.html', phone=phone)

@app.route("/gps/send", methods=['POST'])
def gps_send():

    phone = request.values.get('phone')
    lat = request.values.get('lat')
    long = request.values.get('long')

    return render_template('gps_send.html', phone=phone, lat=lat, long=long)

if __name__ == "__main__":

    # context = ('host.crt', 'host.key')
    app.run(host='0.0.0.0', ssl_context='adhoc', port=6000)
