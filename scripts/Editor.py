# -*- coding: utf-8 -*-
"""
Editor.py
Genera o actualiza el archivo 13-Contenido/Desarrollo.tex
basado en los datos de scripts/Semanas/textos.json
y usando las imágenes ubicadas en scripts/Semanas/pic/.
Compatibilidad con 'datos' como ARREGLO DE OBJETOS.
"""

import os
import json
from textwrap import dedent


# --------------------------------------------------------------------
# === CONFIGURACIÓN ===
# --------------------------------------------------------------------

# Archivo donde se escribirá el bloque LaTeX
OUTPUT_TEX = os.path.join("..", "13-Contenido", "Desarrollo.tex")

# Archivo con los datos base
DATA_FILE = os.path.join("Semanas", "textos.json")

# Carpeta donde están las imágenes
IMG_DIR = os.path.join("Semanas", "pic")


# --------------------------------------------------------------------
# === FUNCIONES PRINCIPALES ===
# --------------------------------------------------------------------
def generar_tabla_semana(semana, insertar_newpage=False):
    """
    Genera el bloque LaTeX de una semana completa.
    - 'semana' contiene campos: id, titulo, datos (lista de registros)
    - Cada elemento de 'datos' genera una fila y bloque de fotos.
    - Si 'insertar_newpage' es True, agrega \\newpage antes del bloque.
    """

    # Arreglo con varios registros dentro de "datos"
    filas_tabla = ""
    registros = semana["datos"]

    for i, d in enumerate(registros):
        # Construir la fila de datos
        fila = dedent(
            f"""
            \\textbf{{{d['fecha']}}} &
            {d['equipo_sistema']} &
            {d['tipo_mantenimiento']} &
            {d['descripcion_trabajo']} &
            {d['personal_directo']} &
            {d['area']} \\\\
            \\hline
            \\multicolumn{{6}}{{|c|}}{{\\textbf{{Registro Fotográfico}}}} \\\\
            \\hline
            \\multicolumn{{6}}{{|c|}}{{ {generar_fotos(d.get('fotos', []))} }} \\\\
            \\hline
            """
        ).strip()
        filas_tabla += fila + "\n"

    bloque = dedent(
        f"""
        { '\\newpage' if insertar_newpage else '' }
        \\subsection{{{semana['titulo']}}}

        \\begin{{table}}[H]
            \\centering
            \\footnotesize
            \\begin{{tabular}}{{|
                >{{\\small\\centering\\arraybackslash}}m{{1.8cm}}|
                >{{\\small\\centering\\arraybackslash}}m{{2.8cm}}|
                >{{\\small\\centering\\arraybackslash}}m{{2.8cm}}|
                >{{\\small}}m{{4cm}}|
                >{{\\small}}m{{2cm}}|
                >{{\\small\\centering\\arraybackslash}}m{{1.2cm}}|
            }}
                \\hline
                \\textbf{{Fecha}} &
                \\textbf{{Equipo / Sistema}} &
                \\textbf{{Tipo de Mantenimiento}} &
                \\centering \\textbf{{Descripción del trabajo realizado}} &
                \\centering \\textbf{{Personal Directo}} &
                \\textbf{{Área}} \\\\
                \\hline\\hline
                {filas_tabla.strip()}
            \\end{{tabular}}
        \\end{{table}}
        """
    ).strip()

    return bloque


def generar_fotos(fotos):
    """Genera el bloque LaTeX con las imágenes de una fila."""
    if not fotos:
        return "Sin registro fotográfico"
    fotos_latex = ""
    for foto in fotos:
        ruta = f"scripts/{IMG_DIR}/{foto}".replace("\\", "/")
        fotos_latex += f"\\includegraphics[width=\\textwidth,keepaspectratio]{{{ruta}}}\n"
    return fotos_latex.strip()


def cargar_datos():
    """Carga los datos desde el archivo JSON."""
    data_path = os.path.join(os.path.dirname(__file__), DATA_FILE)

    if not os.path.exists(data_path):
        raise FileNotFoundError(f"❌ No se encontró el archivo de datos: {data_path}")

    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)


def escribir_en_tex(texto):
    """Guarda el contenido generado en 13-Contenido/Desarrollo.tex."""
    salida_path = os.path.join(os.path.dirname(__file__), OUTPUT_TEX)
    salida_dir = os.path.dirname(salida_path)

    os.makedirs(salida_dir, exist_ok=True)  # asegurarse de que exista
    with open(salida_path, "w", encoding="utf-8") as f:
        f.write(texto)

    print(f"✅ Archivo actualizado correctamente:\n{salida_path}")


# --------------------------------------------------------------------
def main():
    """
    Genera el contenido LaTeX según el JSON:
      - Itera por cada semana.
      - Si cambia 'id', se agrega \\newpage entre bloques.
    """
    semanas = cargar_datos()
    bloques = []

    last_id = None
    for semana in semanas:
        insertar_newpage = last_id is not None and semana["id"] != last_id
        bloques.append(generar_tabla_semana(semana, insertar_newpage))
        last_id = semana["id"]

    contenido_final = "\n\n".join(bloques)
    escribir_en_tex(contenido_final)


# --------------------------------------------------------------------
if __name__ == "__main__":
    main()