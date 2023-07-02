from flask import Flask, jsonify, request
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL configurations
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "pendaftaran"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

# Create MySQL instance
mysql = MySQL(app)


# Get all wargas
@app.route("/warga", methods=["GET"])
def get_wargas():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM wargas")
    wargas = cur.fetchall()
    cur.close()
    return jsonify(wargas)


# Get a specific warga
@app.route("/warga/<int:warga_id>", methods=["GET"])
def get_warga(warga_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM wargas WHERE id = %s", (warga_id,))
    warga = cur.fetchone()
    cur.close()
    if warga is None:
        return jsonify({"error": "Warga not found"}), 404
    return jsonify(warga)


# Create a new warga
@app.route("/warga", methods=["POST"])
def create_warga():
    if not request.json or "nama" not in request.json or "nik" not in request.json:
        return jsonify({"error": "Nama and NIK are required"}), 400
    nama = request.json["nama"]
    nik = request.json["nik"]
    tempat_lahir = request.json.get("tempat_lahir", "")
    tanggal_lahir = request.json.get("tanggal_lahir", "")
    alamat = request.json.get("alamat", "")
    pekerjaan = request.json.get("pekerjaan", "")

    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO wargas (nama, nik, tempat_lahir, tanggal_lahir, alamat, pekerjaan) VALUES (%s, %s, %s, %s, %s, %s)",
        (nama, nik, tempat_lahir, tanggal_lahir, alamat, pekerjaan),
    )
    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "Warga created successfully"})


# Update a warga
@app.route("/warga/<int:warga_id>", methods=["PUT"])
def update_warga(warga_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM wargas WHERE id = %s", (warga_id,))
    warga = cur.fetchone()
    if warga is None:
        cur.close()
        return jsonify({"error": "Warga not found"}), 404

    if not request.json:
        cur.close()
        return jsonify({"error": "No data provided"}), 400

    nama = request.json.get("nama", warga["nama"])
    nik = request.json.get("nik", warga["nik"])
    tempat_lahir = request.json.get("tempat_lahir", warga["tempat_lahir"])
    tanggal_lahir = request.json.get("tanggal_lahir", warga["tanggal_lahir"])
    alamat = request.json.get("alamat", warga["alamat"])
    pekerjaan = request.json.get("pekerjaan", warga["pekerjaan"])

    cur.execute(
        "UPDATE wargas SET nama = %s, nik = %s, tempat_lahir = %s, tanggal_lahir = %s, alamat = %s, pekerjaan = %s WHERE id = %s",
        (nama, nik, tempat_lahir, tanggal_lahir, alamat, pekerjaan, warga_id),
    )
    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "Warga updated successfully"})


# Delete a warga
@app.route("/warga/<int:warga_id>", methods=["DELETE"])
def delete_warga(warga_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM wargas WHERE id = %s", (warga_id,))
    warga = cur.fetchone()
    if warga is None:
        cur.close()
        return jsonify({"error": "Warga not found"}), 404

    cur.execute("DELETE FROM wargas WHERE id = %s", (warga_id,))
    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "Warga deleted successfully"})


if __name__ == "__main__":
    app.run(debug=True)
