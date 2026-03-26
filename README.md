# 📄 Lector de Facturas PRO (v1.1)
**Desarrollado por: Carlos José Carranza V.** *Analista de Sistemas | Software Developer* 📍 Cartagena de Indias, Colombia

---

## ⚠️ Requisito del Sistema
> **IMPORTANTE:** Esta aplicación es **exclusiva para sistemas operativos Windows** (7, 10 u 11). No es compatible con macOS o Linux en su versión ejecutable (.exe).

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
3. **Ejecución:** Al abrirlo, si aparece el mensaje de "Windows protegió su PC", haz clic en **"Más información"** y luego en el botón **"Ejecutar de todas formas"**.

### 2. Flujo de Trabajo (Navegación)
La aplicación te guiará paso a paso mediante ventanas emergentes:

1.  **Selección de Facturas:** Se abrirá una carpeta para que elijas dónde están tus archivos PDF.
2.  **Guardado de Reporte:** Eliges el nombre y la carpeta donde quieres que se cree tu archivo Excel.
3.  **Procesamiento:** La consola mostrará el progreso en tiempo real y los **créditos del desarrollador**.
4.  **Apertura de Archivo:** Al finalizar, el sistema te preguntará si deseas abrir el Excel generado automáticamente.
5.  **Multitarea:** La app te consultará si deseas procesar otra carpeta diferente o si deseas cerrar la herramienta.

---

## 🛠️ Ficha Técnica
- **Motor de extracción:** `pdfplumber` con lógica de proximidad de texto.
- **Formato de Salida:** Microsoft Excel (.xlsx) compatible con todas las versiones.
- **Tratamiento de Moneda:** Adaptado al estándar colombiano (Separadores de miles y decimales).

---

## 👨‍💻 Contacto y Soporte
Si tienes dudas o necesitas una personalización adicional del extractor, puedes contactarme:

- **Email:** [carforck@gmail.com](mailto:carforck@gmail.com)
- **LinkedIn:** [Carlos José Carranza V.](https://www.linkedin.com/in/carranzacarlos/)
- **GitHub:** [carforck](https://github.com/carforck)

*"Tecnología con propósito, innovación con impacto."*
