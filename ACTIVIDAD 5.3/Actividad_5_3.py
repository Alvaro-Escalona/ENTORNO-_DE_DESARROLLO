import tkinter as tk
from tkinter import ttk, messagebox
import requests
import time
import cProfile
import pstats
import io
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class AppEspacialFinal:
    """
    Clase principal para la monitorización de la ISS y análisis de rendimiento.
    
    Esta clase gestiona la interfaz gráfica, las peticiones a la API y la 
    comparación visual entre algoritmos optimizados y no optimizados.
    """

    def __init__(self, root):
        """
        Inicializa la aplicación y configura el estado inicial.

        Args:
            root (tk.Tk): La ventana principal de la aplicación.
        """
        self.root = root
        self.root.title("Examen Tema 5 - Documentación y Optimización")
        self.root.geometry("1150x850")
        
        # Configuración responsiva
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.historico_no_opt = []
        self.historico_opt = []
        self.pasos = []
        self.contador = 0

        self.setup_ui()
        self.bucle_principal()

    def setup_ui(self):
        """
        Configura la interfaz gráfica de usuario (GUI).
        
        Crea dos paneles simétricos con gráficas independientes y cuadros de texto.
        """
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(0, weight=1)

        # Panel Lento
        col_izq = ttk.Labelframe(self.main_frame, text=" VERSIÓN NO OPTIMIZADA ")
        col_izq.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        col_izq.rowconfigure(0, weight=3)
        col_izq.columnconfigure(0, weight=1)

        self.fig_izq, self.ax_izq = plt.subplots(figsize=(4, 3))
        self.canvas_izq = FigureCanvasTkAgg(self.fig_izq, master=col_izq)
        self.canvas_izq.get_tk_widget().grid(row=0, column=0, sticky="nsew")

        self.info_izq = tk.Text(col_izq, height=12, bg="#fff0f0", font=('Consolas', 10))
        self.info_izq.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        ttk.Button(col_izq, text="Help", command=lambda: self.abrir_help("lento")).grid(row=2, column=0, pady=5)

        # Panel Rápido
        col_der = ttk.Labelframe(self.main_frame, text=" VERSIÓN OPTIMIZADA ")
        col_der.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        col_der.rowconfigure(0, weight=3)
        col_der.columnconfigure(0, weight=1)

        self.fig_der, self.ax_der = plt.subplots(figsize=(4, 3))
        self.canvas_der = FigureCanvasTkAgg(self.fig_der, master=col_der)
        self.canvas_der.get_tk_widget().grid(row=0, column=0, sticky="nsew")

        self.info_der = tk.Text(col_der, height=12, bg="#f0fff0", font=('Consolas', 10))
        self.info_der.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        ttk.Button(col_der, text="Help", command=lambda: self.abrir_help("rapido")).grid(row=2, column=0, pady=5)

    def version_lenta(self, datos):
        """
        Ejecuta el procesamiento de datos de forma ineficiente.
        
        Usa bucles redundantes para simular una carga alta de CPU y demostrar
        un rendimiento subóptimo (Complejidad O(n)).

        Args:
            datos (dict): Diccionario crudo obtenido de la API de la ISS.

        Returns:
            tuple: Contiene (latitud, longitud, tiempo_ejecucion).
        """
        inicio = time.perf_counter()
        for _ in range(8500):
            _ = [str(v) for v in datos.values()]
        lat = datos['iss_position']['latitude']
        lon = datos['iss_position']['longitude']
        return lat, lon, time.perf_counter() - inicio

    def version_rapida(self, datos):
        """
        Ejecuta el procesamiento de datos de forma optimizada.
        
        Accede directamente a las claves necesarias del diccionario, minimizando
        los ciclos de reloj (Complejidad O(1)).

        Args:
            datos (dict): Diccionario crudo obtenido de la API de la ISS.

        Returns:
            tuple: Contiene (latitud, longitud, tiempo_ejecucion).
        """
        inicio = time.perf_counter()
        pos = datos.get('iss_position', {})
        lat = pos.get('latitude', '0')
        lon = pos.get('longitude', '0')
        return lat, lon, time.perf_counter() - inicio

    def abrir_help(self, tipo):
        """Muestra los docstrings en una ventana emergente."""
        doc = self.version_rapida.__doc__ if tipo == "rapido" else self.version_lenta.__doc__
        messagebox.showinfo("Docstrings Extraídos", doc)

    def actualizar_graficas(self):
        """Actualiza los ejes de las gráficas con etiquetas y nuevos datos."""
        # Panel Lento
        self.ax_izq.clear()
        self.ax_izq.plot(self.pasos, self.historico_no_opt, color='red', marker='.')
        self.ax_izq.set_title("Eje X: Petición | Eje Y: Segundos")
        self.ax_izq.set_xlabel("Nº de Petición")
        self.ax_izq.set_ylabel("Segundos")
        self.ax_izq.grid(True, alpha=0.3)
        self.canvas_izq.draw()

        # Panel Rápido
        self.ax_der.clear()
        self.ax_der.plot(self.pasos, self.historico_opt, color='green', marker='.')
        self.ax_der.set_title("Eje X: Petición | Eje Y: Segundos")
        self.ax_der.set_xlabel("Nº de Petición")
        self.ax_der.set_ylabel("Segundos (Micro)")
        self.ax_der.grid(True, alpha=0.3)
        self.canvas_der.draw()

    def bucle_principal(self):
        """Ciclo infinito de actualización cada 1.5 segundos."""
        try:
            r = requests.get("http://api.open-notify.org/iss-now.json", timeout=2)
            datos = r.json()
            hora = datetime.now().strftime("%H:%M:%S")

            # Perfilado cProfile
            prof = cProfile.Profile()
            prof.enable()
            lat_o, lon_o, t_o = self.version_rapida(datos)
            prof.disable()
            
            s = io.StringIO()
            ps = pstats.Stats(prof, stream=s).sort_stats('cumulative')
            ps.print_stats()
            
            lat_n, lon_n, t_n = self.version_lenta(datos)

            # Actualizar listas
            self.contador += 1
            self.pasos.append(self.contador)
            self.historico_no_opt.append(t_n)
            self.historico_opt.append(t_o)
            if len(self.pasos) > 25:
                self.pasos.pop(0); self.historico_no_opt.pop(0); self.historico_opt.pop(0)

            # Rellenar Textos
            self.info_izq.delete("1.0", tk.END)
            self.info_izq.insert(tk.END, f" ACTUALIZACIÓN: {hora}\n {'='*30}\n LAT: {lat_n}\n LON: {lon_n}\n TIEMPO: {t_n:.6f}s")
            
            self.info_der.delete("1.0", tk.END)
            self.info_der.insert(tk.END, f" ACTUALIZACIÓN: {hora}\n {'='*30}\n LAT: {lat_o}\n LON: {lon_o}\n TIEMPO: {t_o:.6f}s\n REPORT:\n{s.getvalue()[:100]}")

            self.actualizar_graficas()
        except:
            pass
        self.root.after(1500, self.bucle_principal)

if __name__ == "__main__":
    root = tk.Tk()
    app = AppEspacialFinal(root)
    root.mainloop()
