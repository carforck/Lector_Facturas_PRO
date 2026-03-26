import pdfplumber
import pandas as pd
import os
import re
import sys
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox

# --- INFORMACIÓN DEL DESARROLLADOR ---
# Basado en tu perfil de Analista de Sistemas
CREDITOS = """
----------------------------------------------
   DESARROLLADO POR: CARLOS JOSÉ CARRANZA V.
   Analista de Sistemas | Software Developer
   Contacto: carforck@gmail.com ! +57 3105080356
   Cartagena de Indias, Colombia
----------------------------------------------
"""

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
            
            # Búsqueda mejorada de fecha por proximidad
            patron_fecha = r'(\d{2}[/-]\d{2}[/-]\d{4}|\d{4}[/-]\d{2}[/-]\d{2})'
            keywords_fecha = ["FECHA", "EXPEDICION", "EXPEDICIÓN", "EMISION", "EMISIÓN", "GENERACION", "GENERACIÓN", "FACTURA"]
            
            fecha_encontrada = None
            for idx, linea in enumerate(lineas):
                l_up = linea.upper()
                if "FECHA" in l_up and any(k in l_up for k in keywords_fecha):
                    m = re.search(patron_fecha, linea)
                    if m:
                        fecha_encontrada = m.group(1)
                        break
                    elif idx + 1 < len(lineas):
                        m_debajo = re.search(patron_fecha, lineas[idx+1])
                        if m_debajo:
                            fecha_encontrada = m_debajo.group(1)
                            break
            
            res["Fecha"] = fecha_encontrada if fecha_encontrada else (re.search(patron_fecha, texto_completo).group(1) if re.search(patron_fecha, texto_completo) else "N/A")
            
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
                candidatos = [limpiar_monto_colombia(n) for n in re.findall(r'[\d\.,]{4,}', texto_completo) if limpiar_monto_colombia(n) < 50000000]
                if candidatos: res["Total"] = max(candidatos)
    except Exception as e:
        print(f"Error en {os.path.basename(file_path)}: {e}")
    return res

def seleccionar_origen():
    root = tk.Tk(); root.withdraw(); root.attributes("-topmost", True)
    folder = filedialog.askdirectory(title="1. Selecciona la carpeta con las Facturas PDF")
    root.destroy(); return folder

def seleccionar_destino(folder_inicial):
    root = tk.Tk(); root.withdraw(); root.attributes("-topmost", True)
    nombre_sugerido = f"Reporte_Facturas_{os.path.basename(folder_inicial)}.xlsx"
    file_path = filedialog.asksaveasfilename(
        title="2. ¿Dónde quieres guardar el reporte Excel?",
        defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")], initialfile=nombre_sugerido
    )
    root.destroy(); return file_path

def ejecutar_proceso():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("==============================================")
        print("     EXTRACTOR AUTOMÁTICO DE FACTURAS")
        print(CREDITOS)
        print("==============================================")

        origen = seleccionar_origen()
        if not origen: break

        pdfs = [a for a in os.listdir(origen) if a.lower().endswith('.pdf')]
        if not pdfs:
            messagebox.showwarning("Atención", f"No hay archivos PDF en la carpeta:\n{origen}")
            continue

        destino = seleccionar_destino(origen)
        if not destino: break

        print(f"\n🚀 Procesando {len(pdfs)} archivos...")
        resultados = []
        for i, archivo in enumerate(pdfs, 1):
            print(f" ► [{i}/{len(pdfs)}] Leyendo: {archivo[:40]}...", end="\r", flush=True)
            resultados.append(extraer_datos_v2(os.path.join(origen, archivo)))

        try:
            df = pd.DataFrame(resultados)
            df.to_excel(destino, index=False)
            
            msg = f"Reporte generado con éxito.\nTotal procesado: {len(pdfs)} facturas.\n\n¿Deseas procesar otra carpeta?"
            if not messagebox.askyesno("Proceso Finalizado", msg):
                print("\n🙏 Gracias por utilizar la herramienta. ¡Hasta pronto!")
                messagebox.showinfo("Despedida", "Gracias por utilizar Lector de Facturas PRO.\n\nDesarrollado por Carlos Carranza V.")
                break
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo: {e}")
            if not messagebox.askyesno("Error", "¿Intentar con otra carpeta?"): break

if __name__ == "__main__":
    ejecutar_proceso()