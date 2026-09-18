
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageGrab
from datetime import datetime
import os
import time
import subprocess

class ToromayoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Toromayo")
        
        # --- DISEÑO ULTRA COMPACTO MEDIDAS MODIFICABLE ---
        VENTANA_ANCHO = 180
        VENTANA_ALTO = 250
        
        pantalla_ancho = self.root.winfo_screenwidth()
        pantalla_alto = self.root.winfo_screenheight()
        pos_x = int(pantalla_ancho - (VENTANA_ANCHO + 40))
        pos_y = int((pantalla_alto / 2) - (VENTANA_ALTO / 2))
        self.root.geometry(f"{VENTANA_ANCHO}x{VENTANA_ALTO}+{pos_x}+{pos_y}")
        self.root.resizable(False, False)
        self.root.configure(bg="#070707")
        
        self.lista_capturas = []

        # 1. TÍTULO DE LA EMPRESA TOROMAYO DESARROLLOS APK Y MAS .
        self.lbl_title = tk.Label(root, text="FOTO A PDF", font=("Arial", 16, "bold"), bg="#030303", fg="white")
        self.lbl_title.pack(pady=10)
        
        # 2. BOTÓN: CAPTURAR IMAGEN 
        self.btn_capture = tk.Button(
            root, text="CAPTURADOR DE IMAGEN", font=("Arial", 9, "bold"),
            bg="#1410FF", fg="white", activebackground="#11E3FF", activeforeground="white",
            bd=2, relief="raised", command=self.captura_silenciosa_windows
        )
        self.btn_capture.pack(fill="x", padx=15, pady=4)
        
        # 3. BOTÓN: BORRAR ÚLTIMA
        self.btn_clear = tk.Button(
            root, text="BORRAR", font=("Arial", 12, "bold"),
            bg="#FF1900", fg="white", activebackground="#BD1300", activeforeground="white",
            bd=2, relief="raised", command=self.borrar_ultima_captura
        )
        self.btn_clear.pack(fill="x", padx=15, pady=4)
        
        # 4. RECUADRO NUMÉRICO (CONTADOR)
        self.display_frame = tk.Frame(root, bg="white", bd=2, relief="sunken")
        self.display_frame.pack(fill="both", expand=True, padx=15, pady=8)
        
        self.lbl_number = tk.Label(self.display_frame, text="0", font=("Arial", 34, "bold"), bg="white", fg="#050505")
        self.lbl_number.pack(expand=True)
        
        # 5. BOTÓN ÚNICO: GUARDAR PDF
        self.btn_pdf = tk.Button(
            root, text="GUARDAR PDF", font=("Arial", 12, "bold"),
            bg="#F11FE0", fg="white", activebackground="#9C0D7D", activeforeground="white",
            bd=2, relief="raised", command=self.generar_pdf
        )
        self.btn_pdf.pack(fill="x", padx=15, pady=(4, 15))

    def captura_silenciosa_windows(self):
        self.root.withdraw()
        self.root.update()
        time.sleep(0.2)
        
        # Limpiar portapapeles
        ImageGrab.grabclipboard()
        
        # Ejecuta la interfaz de recorte directo de región en Windows
        subprocess.Popen("snippingtool /clip", shell=True)
        
        img_capturada = None
        for _ in range(40):  
            time.sleep(0.4)
            img_capturada = ImageGrab.grabclipboard()
            if isinstance(img_capturada, Image.Image):
                break
        
        if isinstance(img_capturada, Image.Image):
            nombre_archivo = f"captura_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            img_capturada.save(nombre_archivo, "PNG", compress_level=0)
            
            if os.path.exists(nombre_archivo):
                self.lista_capturas.append(nombre_archivo)
                self.lbl_number.config(text=str(len(self.lista_capturas)))
        else:
            messagebox.showwarning("Toromayo", "No se detectó el recorte o se canceló.")
            
        self.root.deiconify()

    def borrar_ultima_captura(self):
        if self.lista_capturas:
            archivo_a_borrar = self.lista_capturas.pop()
            if os.path.exists(archivo_a_borrar):
                os.remove(archivo_a_borrar)
            self.lbl_number.config(text=str(len(self.lista_capturas)))
        else:
            messagebox.showwarning("Toromayo", "No hay capturas en el historial.")

    # --- REMUESTREO EN ULTRA DENSIDAD MÁXIMA (8K SIMULADO - CORREGIDO) ---
    def generar_pdf(self):
        if not self.lista_capturas:
            messagebox.showwarning("Toromayo", "No tienes capturas para armar el documento.")
            return
        try:
            imagenes_pil = []
            for f in self.lista_capturas:
                img = Image.open(f).convert("RGB")
                
                # ESCALADO ULTRA MASIVO 8X 
                nuevo_ancho = img.width * 8
                nuevo_alto = img.height * 8
                img_alta_res = img.resize((nuevo_ancho, nuevo_alto), Image.Resampling.LANCZOS)
                imagenes_pil.append(img_alta_res)
            
            carpeta_documentos = os.path.join(os.path.expanduser("~"), "Documents")
            nombre_pdf = os.path.join(carpeta_documentos, f"Reporte_Toromayo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
            
            opciones_guardado = {
                "dpi": (1200, 1200),     # Resolución masiva de imprenta
                "quality": 100,          
                "subsampling": 0         
            }
            
            # CORRECCIÓN CLAVE: Acceso correcto al primer elemento de la lista para inicializar el PDF
            if len(imagenes_pil) == 1:
                imagenes_pil[0].save(nombre_pdf, **opciones_guardado)
            else:
                imagenes_pil[0].save(nombre_pdf, save_all=True, append_images=imagenes_pil[1:], **opciones_guardado)
            
            for f in self.lista_capturas:
                if os.path.exists(f):
                    os.remove(f)
            
            messagebox.showinfo("Éxito", f"¡PDF Generado en Máxima Densidad (8K Simulado)!\nGuardado en Documentos\nArchivo: {os.path.basename(nombre_pdf)}")
            
            self.lista_capturas.clear()
            self.lbl_number.config(text="0")
        except Exception as e:
            messagebox.showerror("Error PDF", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = ToromayoApp(root)
    root.mainloop()
