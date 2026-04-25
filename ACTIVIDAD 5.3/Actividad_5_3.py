import tkinter as tk
from tkinter import ttk
import requests
import time
import cProfile
import pstats
import io

class AppEspacial:
    """
    Clase principal para la aplicación de comparación de optimización.
    Muestra datos de la ISS comparando dos métodos de procesamiento.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Comparación de Optimización - ISS")
        self.root.geometry("800x500")
        
        # Configuración de la interfaz (Tkinter)
        self.setup_ui()
        
    def setup_ui(self):
        """Configura la división de la pantalla en dos paneles."""
        main_frame = ttk.Panedwindow(self.root, orient=tk.HORIZONTAL)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Panel Izquierdo: No Optimizado
        self.panel_no_opt = ttk.Labelframe(main_frame, text="Versión NO Optimizada")
        self.label_no_opt = ttk.Label(self.panel_no_opt, text="Esperando datos...", wraplength=350)
        self.label_no_opt.pack(padx=10, pady=10)
        main_frame.add(self.panel_no_opt)

        # Panel Derecho: Optimizado
        self.panel_opt = ttk.Labelframe(main_frame, text="Versión Optimizada")
        self.label_opt = ttk.Label(self.panel_opt, text="Esperando datos...", wraplength=350)
        self.label_opt.pack(padx=10, pady=10)
        main_frame.add(self.panel_opt)

        # Botón de actualización
        self.btn_update = ttk.Button(self.root, text="Actualizar Datos", command=self.ejecutar_comparacion)
        self.btn_update.pack(pady=10)

    def obtener_datos_api(self):
        """Obtiene la posición de la ISS desde una API pública."""
        try:
            response = requests.get("http://api.open-notify.org/iss-now.json", timeout=5)
            return response.json()
        except Exception as e:
            return None

    def version_no_optimizada(self, datos):
        """
        Procesamiento ineficiente: uso excesivo de bucles y conversiones innecesarias.
        """
        inicio = time.time()
        # Simulación de cálculos repetidos y bucles innecesarios
        resultado = []
        for _ in range(1000):
            temp_list = []
            for clave in datos.keys():
                temp_list.append(datos[clave])
            resultado.append(temp_list[0])
        
        lat = datos['iss_position']['latitude']
        lon = datos['iss_position']['longitude']
        fin = time.time()
        return f"Lat: {lat}\nLon: {lon}\nTiempo: {fin-inicio:.6f}s"

    def version_optimizada(self, datos):
        """
        Procesamiento eficiente: acceso directo y funciones integradas de Python.
        """
        inicio = time.time()
        # Uso de acceso directo por clave y estructuras adecuadas
        posicion = datos.get('iss_position', {})
        lat = posicion.get('latitude')
        lon = posicion.get('longitude')
        fin = time.time()
        return f"Lat: {lat}\nLon: {lon}\nTiempo: {fin-inicio:.6f}s"

    def ejecutar_comparacion(self):
        """Ejecuta ambas versiones y muestra los resultados."""
        datos = self.obtener_datos_api()
        if datos:
            self.label_no_opt.config(text=self.version_no_optimizada(datos))
            self.label_opt.config(text=self.version_optimizada(datos))
            
            # Análisis con cProfile (Requisito de la actividad)
            pr = cProfile.Profile()
            pr.enable()
            self.version_optimizada(datos)
            pr.disable()
            pr.print_stats(sort='time')

if __name__ == "__main__":
    root = tk.Tk()
    app = AppEspacial(root)
    root.mainloop()