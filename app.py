from flask import Flask, render_template, request, send_file
import pandas as pd
import io

app = Flask(__name__)

archivo_en_memoria = None
nombre_descarga = "datos_limpios.csv"

@app.route("/", methods=["GET", "POST"])
def home():
    global archivo_en_memoria, nombre_descarga

    if request.method == "POST":

        archivo = request.files["archivo"]

        if archivo.filename == "":
            return "No seleccionaste archivo"

        # 🔥 nombre original
        nombre_original = archivo.filename.replace(".csv", "")
        nombre_descarga = f"{nombre_original}_limpio.csv"

        df = pd.read_csv(archivo)

        filas_antes = len(df)

        # limpiar espacios
        for col in df.select_dtypes(include="object").columns:
            df[col] = df[col].str.strip()

        # eliminar filas vacías
        df = df.dropna(how="all")

        # eliminar duplicados
        df = df.drop_duplicates()

        # filtrar emails inválidos
        if "email" in df.columns:
            df = df[df["email"].str.contains("@", na=False)]

        filas_despues = len(df)
        eliminadas = filas_antes - filas_despues

        # memoria
        output = io.StringIO()
        df.to_csv(output, index=False)
        output.seek(0)

        archivo_en_memoria = io.BytesIO(output.getvalue().encode())

        return render_template(
            "resultado.html",
            antes=filas_antes,
            despues=filas_despues,
            eliminadas=eliminadas
        )

    return render_template("index.html")


@app.route("/descargar")
def descargar():
    return send_file(
        archivo_en_memoria,
        as_attachment=True,
        download_name=nombre_descarga,
        mimetype="text/csv"
    )


if __name__ == "__main__":
    app.run(debug=True)