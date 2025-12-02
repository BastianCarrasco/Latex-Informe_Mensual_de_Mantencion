import os

# === CONFIGURACIÓN ===
# Ruta relativa al archivo que quieres editar
TEX_FILE_PATH = os.path.join("..", "13-Contenido", "test.tex")


def leer_tex(path=TEX_FILE_PATH):
    """Leer el contenido actual del archivo .tex."""
    if not os.path.exists(path):
        print(f"❌ No se encontró el archivo: {path}")
        return ""
    with open(path, "r", encoding="utf-8") as f:
        contenido = f.read()
    print("📖 Archivo leído correctamente.")
    return contenido


def escribir_tex(nuevo_texto: str, path=TEX_FILE_PATH):
    """Sobrescribir el archivo .tex con nuevo contenido."""
    with open(path, "w", encoding="utf-8") as f:
        f.write(nuevo_texto)
    print(f"✅ Archivo sobrescrito: {path}")


def agregar_contenido(linea: str, path=TEX_FILE_PATH):
    """
    Agrega una nueva línea o bloque de texto al final del archivo.
    """
    with open(path, "a", encoding="utf-8") as f:
        f.write("\n" + linea.strip() + "\n")
    print(f"✍️ Línea agregada a {path}")


def ejemplo_uso():
    # 1. Leer contenido existente
    contenido = leer_tex()
    print("\n--- Contenido actual ---")
    print(contenido if contenido else "(vacío)")

    # 2. Agregar un nuevo bloque LaTeX
    nuevo_bloque = r"""
\section{Nueva sección creada con Python}
Este texto fue insertado automáticamente usando un script en Python.
Podemos incluir fórmulas como \( E = mc^2 \) o listas:

\begin{itemize}
  \item Primer ítem
  \item Segundo ítem
\end{itemize}
"""
    agregar_contenido(nuevo_bloque)

    # 3. Verificar resultado
    print("\n✅ Nuevo contenido agregado con éxito.")


if __name__ == "__main__":
    ejemplo_uso()