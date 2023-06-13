# Fungsi untuk menyimpan gambar dari request, return image path
def saveImage(request):
    import os
    from dotenv import load_dotenv

    load_dotenv()
    image_file = request.files["image"]
    image_path = os.path.join(os.getenv("UPLOAD_FOLDER"), image_file.filename)
    image_file.save(image_path)
    return image_path


def predict(model, image_path):
    from tensorflow import keras
    import cv2  # import library
    import numpy as np
    import json, os

    image_size = (224, 224)  # Semua input di convert ke size ini

    # Load Image
    img = cv2.imread(image_path)  # load image
    img = cv2.resize(img, image_size)  # resize
    img = (
        img.astype("float32") / 255.0
    )  # Convert dan normalize sehingga menjadi antara 0-1
    img = np.expand_dims(img, axis=0)  # tambah 1 dimensi

    predictions = model.predict(img)  # ngepredict dengan model

    class_labels = [
        "Bengal",
        "Bombay",
        "Persian",
        "Torbie",
        "Tuxedo",
    ]  # Ini untuk label output

    for i, prediction in enumerate(predictions[0]):  # Iterasi ke semua hasil prediksi
        class_label = class_labels[i]
        confidence = prediction * 100  # Sehingga bentuk persen
        print("Class:", class_label)
        print("Confidence:", confidence, "%")

    predicted_class_index = np.argmax(
        predictions[0]
    )  # Urutkan ke terbesar untuk dapat hasil terbaik
    predicted_class_label = class_labels[predicted_class_index]
    highest_confidence = predictions[0][predicted_class_index] * 100

    os.remove(image_path)

    data = {}
    data["label"] = predicted_class_label
    data["percentage"] = highest_confidence
    return data


def getCat(getAll=True, label=""):
    import os
    import mysql.connector
    from dotenv import load_dotenv

    load_dotenv()

    # Configure the MySQL database connection
    db = mysql.connector.connect(
        host=os.getenv("HOST"),
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
        database=os.getenv("DATABASE"),
    )

    # Create a cursor object to interact with the database
    cursor = db.cursor()

    # Execute a SELECT query
    if getAll:
        query = "SELECT * FROM cats"
    else:
        query = "SELECT * FROM cats where cat_race like '" + label + "'"
    cursor.execute(query)

    # Fetch all the rows returned by the query
    data = cursor.fetchall()

    # Convert the data to a JSON response
    result = []
    for row in data:
        result.append(
            {
                "catId": row[0],
                "catRaces": row[1],
                "catDesc": row[2],
                "catCare": row[3],
                # Add more columns as needed
            }
        )

    # Close the cursor and database connection
    cursor.close()
    db.close()

    # Return the JSON response
    return result
