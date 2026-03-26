import pdfplumber
import pandas as pd
import os
import re
import sys
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox

# --- FUNCIONES DE LIMPIEZA Y EXTRACCIÓN ---
def limpiar_monto_colombia(texto):
    if not texto: return 0
    limpio = re.sub(r'[^\d,.]', '', texto).strip()
    if not limpio: return 0
    if ('.' in limpio and ',' in limpio):
        if limpio.rfind(',') > limpio.rfind('.'):
            limpio = limpio.replace('.', '').replace(',', '.')
        else:
            limpio = limpio.replace(',', '')
    elif ',' in limpio:
        partes = limpio.split(',')
        if len(partes[-1]) == 3: limpio = limpio.replace(',', '')
        else: limpio = limpio.replace(',', '.')
    elif '.' in limpio:
        partes = limpio.split('.')
        if len(partes[-1]) == 3: limpio = limpio.replace('.', '')
    try:
        return round(float(limpio), 2)
    except:
        return 0

def extraer_datos_v2(file_path):
    res = {"Archivo": os.path.basename(file_path), "Proveedor": "N/A", "NIT": "N/A", "Fecha": "N/A", "Subtotal": 0, "Total": 0}
    try:
        with pdfplumber.open(file_path) as pdf:
            texto_completo = ""
            for p in pdf.pages:
                texto_completo += (p.extract_text(layout=True) or "") + "\n"
            lineas = [l.strip() for l in texto_completo.split('\n') if l.strip()]
            
            nit_pattern = re.search(r'(\d{9}-\d|\d{3}\.\d{3}\.\d{3}-\d|\d{9})', texto_completo)
            if nit_pattern: res["NIT"] = nit_pattern.group(1)
            
            palabras_basura = ["FACTURA", "ELECTRÓNICA", "VENTA", "FECHA", "PAG", "CLIENTE", "NIT", "TEL", "CEL", "ORIGINAL", "DOCUMENTO"]
            for l in lineas[:15]:
                if len(l) > 5 and not any(x in l.upper() for x in palabras_basura):
                    if len(re.findall(r'\d', l)) < len(l) / 3:
                        res["Proveedor"] = l[:60]
                        break
            
            fecha_m = re.search(r'(\d{2}[/-]\d{2}[/-]\d{4}|\d{4}[/-]\d{2}[/-]\d{2})', texto_completo)
            if fecha_m: res["Fecha"] = fecha_m.group(1)
            
            for linea in lineas:
                l_up = linea.upper()
                if any(x in l_up for x in ["TOTAL", "A PAGAR", "VALOR NETO"]):
                    nums = re.findall(r'[\d\.,]{4,}', linea)
                    if nums:
                        val = limpiar_monto_colombia(nums[-1])
                        if val > res["Total"]: res["Total"] = val
                if any(x in l_up for x in ["SUBTOTAL", "VALOR BRUTO"]):
                    nums = re.findall(r'[\d\.,]{4,}', linea)
                    if nums: res["Subtotal"] = limpiar_monto_colombia(nums[-1])
            
            if res["Total"] == 0:
                todos_nums = re.findall(r'[\d\.,]{4,}', texto_completo)
                candidatos = [limpiar_monto_colombia(n) for n in todos_nums if limpiar_monto_colombia(n) < 50000000]
                if candidatos: res["Total"] = max(candidatos)
    except Exception as e:
        print(f"Error procesando {os.path.basename(file_path)}: {e}")
    return res

# --- CONFIGURACIÓN DE VENTANAS ---
def seleccionar_origen():
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    folder = filedialog.askdirectory(title="1. Selecciona la carpeta con las Facturas PDF")
    root.destroy()
    return folder

def seleccionar_destino(folder_inicial):
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    nombre_sugerido = f"Reporte_Facturas_{os.path.basename(folder_inicial)}.xlsx"
    file_path = filedialog.asksaveasfilename(
        title="2. ¿Dónde quieres guardar el reporte Excel?",
        defaultextension=".xlsx",
        filetypes=[("Excel files", "*.xlsx")],
        initialfile=nombre_sugerido
    )
    root.destroy()
    return file_path

# --- PROCESO PRINCIPAL ---
print("==============================================")
print("     EXTRACTOR AUTOMÁTICO DE FACTURAS")
print("==============================================")

origen = seleccionar_origen()
if not origen:
    print("❌ Proceso cancelado.")
    sys.exit()

pdfs = [a for a in os.listdir(origen) if a.lower().endswith('.pdf')]
if not pdfs:
    print(f"❌ No hay PDFs en: {origen}")
    input("Presiona ENTER para salir...")
    sys.exit()

destino = seleccionar_destino(origen)
if not destino:
    print("❌ No se seleccionó destino.")
    sys.exit()

print(f"\n🚀 Iniciando lectura de {len(pdfs)} archivos...")
print("----------------------------------------------")

resultados = []
for i, archivo in enumerate(pdfs, 1):
    # El flush=True obliga a la terminal a mostrar el texto de inmediato
    print(f" ► [{i}/{len(pdfs)}] Leyendo: {archivo[:40]}...", end="\r", flush=True)
    
    ruta_completa = os.path.join(origen, archivo)
    datos = extraer_datos_v2(ruta_completa)
    resultados.append(datos)

print(f"\n\n✨ ¡Lectura completada!")

# --- GUARDAR EXCEL ---
try:
    df = pd.DataFrame(resultados)
    df.to_excel(destino, index=False)
    
    print("----------------------------------------------")
    print(f"📊 Reporte guardado: {os.path.basename(destino)}")
    print(f"💰 Suma Total Detectada: ${df['Total'].sum():,.2f}")
    print("----------------------------------------------")
    
    if messagebox.askyesno("Éxito", f"Proceso terminado.\n\n¿Deseas abrir el Excel ahora?"):
        if sys.platform == "win32":
            os.startfile(destino)
        else:
            subprocess.call(["xdg-open", destino])

except Exception as e:
    print(f"❌ Error al guardar Excel: {e}")
    messagebox.showerror("Error", f"No se pudo guardar el archivo Excel:\n{e}")

print("\nPresiona ENTER para finalizar y cerrar esta ventana...")
input()