from flask import Flask, request, jsonify

from pyexcel_ods import get_data

app=Flask(__name__)

@app.route("/read", methods=['GET'])
def read_records():
    ods_data = get_data("test.ods")
    ret_data = {}

    for sheet in ods_data:
        if sheet == 'humanactivity.weaponsequipment.trap':
            ret_data[sheet] = []
            for row_no, row in enumerate(ods_data[sheet]):
                if row_no > 0:
                    ret_data[sheet].append(row)

    # return jsonify(ret_data)
    # return jsonify((ods_data[sheet]))
    return jsonify((ods_data))

if __name__ == "__main__":
    app.run()
