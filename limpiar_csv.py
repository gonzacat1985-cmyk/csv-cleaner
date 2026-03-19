import pandas as pd
import re

df = pd.read_csv("datos.csv")

# limpiar espacios
for col in df.select_dtypes(include=["object","string"]).columns:
    df[col] = df[col].str.strip()

# eliminar duplicados
df = df.drop_duplicates()

# eliminar filas vacías
df = df.dropna(how="all")

# función para validar emails
def email_valido(email):
    patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(patron, str(email)) is not None

# filtrar emails inválidos
if "email" in df.columns:
    df = df[df["email"].apply(email_valido)]

print("Filas finales:", len(df))

# guardar resultado
df.to_csv("datos_limpios.csv", index=False)

print("Archivo guardado: datos_limpios.csv")
print("CSV limpiado con éxito")