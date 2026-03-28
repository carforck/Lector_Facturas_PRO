# 📄 Lector de Facturas PRO (v1.1)
**Desarrollado por: Carlos José Carranza V.**  
*Analista de Sistemas | Software Developer*  
📍 Cartagena de Indias, Colombia

---

## 🧾 Descripción General
**Lector de Facturas PRO** es una herramienta diseñada para automatizar la extracción de información clave desde archivos PDF de facturación, permitiendo generar reportes estructurados en Excel de forma rápida, precisa y eficiente.

Ideal para áreas contables, administrativas o procesos de auditoría.

---

## ⚠️ Requisito del Sistema
> **IMPORTANTE:** Esta aplicación es **exclusiva para sistemas operativos Windows** (7, 10 u 11).  
> ❌ No es compatible con macOS o Linux en su versión ejecutable (.exe).

---

## ✨ Características Principales
- 📂 Procesamiento masivo de múltiples archivos PDF
- ⚡ Extracción automática de datos relevantes
- 📊 Generación de reportes en Excel (.xlsx)
- 🔍 Validación inteligente de valores (Subtotal y Total)
- 🧠 Lógica optimizada para diferentes formatos de factura
- 🖥️ Interfaz guiada paso a paso (sin necesidad de conocimientos técnicos)

---

## 📊 Datos que extrae del PDF

El algoritmo está diseñado para identificar y organizar los siguientes puntos clave de cada factura:

| Campo | Descripción |
| :--- | :--- |
| **Archivo** | Nombre original del documento PDF procesado. |
| **Proveedor** | Nombre o Razón Social de la empresa que emite la factura. |
| **NIT** | Número de Identificación Tributaria del emisor (con o sin dígito de verificación). |
| **Fecha** | Fecha oficial del documento (Prioriza: Fecha de factura, expedición o emisión). |
| **Subtotal** | Valor antes de impuestos (si está disponible de forma clara). |
| **Total** | Valor neto a pagar (calculado mediante validación de montos máximos). |

---

## 🚀 Guía de Uso para el Usuario

### 1. Instalación
1. Ve a la sección de [**Última Versión (Releases)**](https://github.com/carforck/Lector_Facturas_PRO/releases/latest).
2. Descarga el archivo: `Lector_Facturas_PRO_Carranza.exe`.
3. Ejecuta el archivo descargado.

> ⚠️ Si Windows muestra el mensaje **"Windows protegió su PC"**:
> - Haz clic en **"Más información"**
> - Luego selecciona **"Ejecutar de todas formas"**

---

### 2. Flujo de Trabajo (Navegación)

La aplicación te guiará paso a paso mediante ventanas emergentes:

1. **Selección de Facturas:**  
   Selecciona la carpeta donde se encuentran los archivos PDF.

2. **Guardado de Reporte:**  
   Define el nombre y la ubicación del archivo Excel de salida.

3. **Procesamiento:**  
   La consola mostrará el progreso en tiempo real y los créditos del desarrollador.

4. **Apertura de Archivo:**  
   Podrás abrir automáticamente el archivo Excel generado.

5. **Multitarea:**  
   Decide si deseas procesar otra carpeta o cerrar la aplicación.

---

## 🛠️ Ficha Técnica
- **Lenguaje base:** Python
- **Motor de extracción:** `pdfplumber`
- **Lógica:** Análisis por proximidad de texto y patrones
- **Formato de salida:** Microsoft Excel (.xlsx)
- **Librerías principales:**
  - `pdfplumber`
  - `pandas`
  - `openpyxl`
- **Tratamiento de moneda:** Adaptado al estándar colombiano (separadores de miles y decimales)

---

## ⚙️ Manejo de Errores
La aplicación contempla escenarios comunes como:

- ❌ PDFs corruptos o no legibles  
- ❌ Facturas con formatos no reconocidos  
- ❌ Campos faltantes o inconsistentes  

En estos casos:
- Se registran en consola
- No detienen el procesamiento general
- Se continúa con los demás archivos

---

## 📌 Buenas Prácticas de Uso
- Mantener los PDFs en una sola carpeta
- Evitar nombres de archivos con caracteres especiales
- Verificar que los documentos sean facturas legibles (no imágenes escaneadas sin OCR)

---

## 🧭 Roadmap (Próximas Mejoras)
- 🌐 Compatibilidad con macOS y Linux
- 🤖 Integración con OCR para PDFs escaneados
- 📊 Dashboard visual de resultados
- ☁️ Exportación a Google Sheets
- 🧩 Soporte para más formatos de factura (multi-país)

---

## 👨‍💻 Contacto y Soporte

Si tienes dudas o necesitas una personalización adicional del extractor, puedes contactarme:

- 📧 **Email:** [carforck@gmail.com](mailto:carforck@gmail.com)  
- 💼 **LinkedIn:** [Carlos José Carranza V.](https://www.linkedin.com/in/carranzacarlos/)  
- 🧑‍💻 **GitHub:** [carforck](https://github.com/carforck)

---

## 📄 Licencia
Este proyecto es de uso privado/distribución controlada.  
Para licencias comerciales o uso empresarial, contactar directamente al desarrollador.

---

> *"Tecnología con propósito, innovación con impacto."*
