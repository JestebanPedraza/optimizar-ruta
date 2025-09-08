# 🚗 Optimizador de Rutas con Python

Este proyecto contiene un script en **Python** que calcula la **ruta más óptima** entre varios puntos leídos desde un archivo Excel.  
Se implementan dos algoritmos clásicos:  
- 🔹 **Vecino más cercano**  
- 🔹 **2-Opt** (optimización adicional para mejorar la ruta inicial)  

El resultado es un archivo `.txt` con el orden recomendado de los puntos a visitar.

---

## 📥 Instrucciones para ejecutar el programa

1. **Descargar el repositorio**  
   Haz clic en el botón verde **Code** y selecciona **Download ZIP**.  
   Extrae el contenido en la carpeta en tu PC.

2. **(Opcional) Eliminar archivos innecesarios**  
   Si solo deseas ejecutar el programa y **no modificar el código**, puedes borrar los archivos:  
   - `main.py`  
   - `requirements.txt`  

3. **Preparar el archivo Excel**  
   - Abre el Excel incluido en el repositorio o crea uno con los siguientes campos:  
     - **id** → identificador único del punto  
     - **latitud**  
     - **longitud**  
   - ⚠️ Recomendación: establece el formato de las celdas como **Texto** para evitar problemas de lectura.  
   - Guarda y cierra el archivo.

4. **Ejecutar el programa**  
   - Ve a la carpeta **`dist/`**  
   - Haz doble clic en **`main.exe`**

5. **Consultar los resultados**  
   - Se generará automáticamente un archivo **`.txt`** con la ruta más óptima.

---

## 🛠️ Tecnologías utilizadas
- Python 3
- Algoritmos de optimización de rutas: *Vecino más cercano* + *2-Opt*
- Lectura de datos desde Excel (`openpyxl`)

---

## 📌 Notas
- Si deseas **modificar o mejorar el script**, conserva los archivos `main.py` y `requirements.txt`.
- El ejecutable fue generado para simplificar el uso y no requiere instalar Python en tu máquina.

---

## ✨ Autor
Proyecto desarrollado por [Esteban Pedraza](https://github.com/JestebanPedraza)
