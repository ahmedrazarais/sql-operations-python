from flask import Flask,request,jsonify
import mysql.connector
from config import DB_HOST,DB_PASSWORD,DB_USER
app=Flask(__name__)


try:
    conn=mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database="operations"
    )
    cursor=conn.cursor()

        
except mysql.connector.Error as e:
    print(f"Error in connection {e}")
    exit()




@app.route("/project",methods=["GET"])
def get_data():
    """
    Retrieve all records from the 'admin' table.

    Returns:
        tuple: A tuple containing:
            - list: A list of dictionaries representing the retrieved records.
            - int: HTTP status code indicating the success or failure of the request.
        
        Possible HTTP status codes:
            - 200: Successful retrieval of records.
            - 404: No records found in the database.
    """
    global cursor
    if request.method=="GET":
        cursor.execute("SELECT * FROM admin ")
        rows=cursor.fetchall()
        if len(rows)>=1:
          data = [{"id": row[0], "name": row[1], "city": row[2], "subject": row[3]} for row in rows]
          return jsonify(data), 200
         
        else:
            return "Nothing found",404
        

@app.route("/project",methods=["POST"])
def add_data():
    """
    Add a new record to the 'admin' table.

    Request Body:
        - id (int): The ID of the new record.
        - name (str): The name of the new record.
        - city (str): The city of the new record.
        - subject (str): The subject of the new record.

    Returns:
        tuple: A tuple containing:
            - dict: A dictionary containing a success message if the data is added successfully.
            - int: HTTP status code indicating the success or failure of the request.
        
        Possible HTTP status codes:
            - 201: Successful addition of data.
            - 400: Bad request (e.g., if the provided ID already exists).
    """
    global cursor
    if request.method=="POST":
        id=request.form["id"]
        name=request.form["name"]
        city=request.form["city"]
        subject=request.form["subject"]
        # Check if the id already exists in the database
        cursor.execute("SELECT id FROM admin WHERE id = %s", (id,))
        existing_id = cursor.fetchone()
        if existing_id:
            return jsonify({"error": f"ID {id} already exists"}), 400


        query="INSERT INTO admin (id,name,city,subject) VALUES (%s,%s,%s,%s)"
        cursor.execute(query,(id,name,city,subject))
        conn.commit()
        return jsonify({"message": "Data added successfully"}), 201



@app.route("/project/<int:input_id>",methods=['DELETE'])
def delete_record(input_id):
    """
    Delete a record from the 'admin' table based on the provided ID.

    Args:
        input_id (int): The ID of the record to be deleted.

    Returns:
        tuple: A tuple containing:
            - dict or str: A dictionary with a success message if the record is deleted successfully, or a string indicating an error message.
            - int: HTTP status code indicating the success or failure of the request.
        
        Possible HTTP status codes:
            - 201: Successful deletion of the record.
            - 404: Record not found in the database.
    """
    global cursor
    if request.method=="DELETE":
        cursor.execute("SELECT * FROM admin")
        rows=cursor.fetchall()
        if len(rows)>=1:
            for row in rows:
                if row[0]==input_id:
                    query=("DELETE FROM admin WHERE id=%s")
                    cursor.execute(query,(input_id,))
                    conn.commit()
                    return jsonify("meggage row deleted succesfully"),201
                else:
                    return "nothing found",404
        else:
            return "nothing found empty database",404


@app.route("/project/<int:row_id>", methods=["PUT"])
def update_data(row_id):
    """
    Update a record in the 'admin' table based on the provided ID.

    Args:
        row_id (int): The ID of the record to be updated.

    Returns:
        tuple: A tuple containing:
            - dict or str: A dictionary with a success message if the record is updated successfully, or a string indicating an error message.
            - int: HTTP status code indicating the success or failure of the request.
        
        Possible HTTP status codes:
            - 200: Successful update of the record.
            - 400: Bad request (e.g., if no data is provided for update).
            - 500: Internal server error (e.g., database error).
    """
  
    global cursor, conn
    if request.method == "PUT":
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Construct the update query dynamically based on the provided fields in the JSON data
        update_query = "UPDATE admin SET "
        update_values = []
        for key, value in data.items():
            if key in ["id", "name", "city", "subject"]:
                update_query += f"{key} = %s, "
                update_values.append(value)

        # Check if any valid fields were provided for update
        if not update_values:
            return jsonify({"error": "No valid fields provided for update"}), 400

        # Complete the update query and execute it
        update_query = update_query.rstrip(", ") + " WHERE id = %s"
        update_values.append(row_id)
        try:
            cursor.execute(update_query, tuple(update_values))
            conn.commit()
            return jsonify({"message": f"Record with ID {row_id} updated successfully"}), 200
        except mysql.connector.Error as e:
            return jsonify({"error": f"Failed to update record: {e}"}), 500

        
       

if __name__=="__main__":
    app.run(debug=True)

    
            

