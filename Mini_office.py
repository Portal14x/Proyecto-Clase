import os
import speech_recognition as sr

from PySide6.QtGui import QAction, QIcon, QKeySequence, QFont, QTextCursor
from PySide6.QtWidgets import QApplication, QMainWindow, QToolBar, QTextEdit, QInputDialog, QFileDialog
from PySide6.QtCore import Qt, QSize
from contadorWidget import WordCounterWidget

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mini Word")
        self.archivo_actual = None
        # Crear barra de menús
        barra_menus = self.menuBar()
        menu = barra_menus.addMenu("&Archivo")
        editar = barra_menus.addMenu("&Editar")
        
        # Crear área de texto
        self.texto = QTextEdit(self)
        self.texto.textChanged.connect(self.actualizar_contador)
        self.setCentralWidget(self.texto)

        # Crear barra de estado
        self.status = self.statusBar()
        self.mensaje_estado = "" 
        
        self.widget_contador = WordCounterWidget(parent=self)
        self.status.addPermanentWidget(self.widget_contador)
        
        # Menu Archivo
        accionNu = QAction("Nuevo", self)
        accionAb = QAction("Abrir", self)
        accionGu = QAction("Guardar", self)
        accionSa = QAction("Salir", self)
        accionSa.triggered.connect(self.close)

        accionNu.triggered.connect(self.HerNuevo)
        accionAb.triggered.connect(self.HerAbrir)
        accionGu.triggered.connect(self.HerGuardar)

        # Menu Editar
        editarDes = QAction("Deshacer", self)
        editarDes.setShortcut(QKeySequence("Ctrl+z"))
        editarDes.triggered.connect(self.Deshacer)
        
        editarRe = QAction("Rehacer", self)
        editarRe.setShortcut(QKeySequence("Ctrl+b"))
        editarRe.triggered.connect(self.Rehacer)
        
        editarCop = QAction("Copiar", self)
        editarCop.setShortcut(QKeySequence("Ctrl+c"))
        editarCop.triggered.connect(self.Copiar)
        
        editarCor = QAction("Cortar", self)
        editarCor.setShortcut(QKeySequence("Ctrl+x"))
        editarCor.triggered.connect(self.Cortar)
        
        editarPe = QAction("Pegar", self)
        editarPe.setShortcut(QKeySequence("Ctrl+v"))
        editarPe.triggered.connect(self.Pegar)
        
        editar.addAction(editarDes)
        editar.addAction(editarRe)
        editar.addAction(editarCop)
        editar.addAction(editarCor)        
        editar.addAction(editarPe)

        menu.addAction(accionNu)
        menu.addAction(accionAb)
        menu.addAction(accionGu)
        menu.addAction(accionSa)
        
        # Crear Barra herramientas
        barra_herramientas = QToolBar("Barra de herramientas 1")
        barra_herramientas.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        barra_herramientas.setIconSize(QSize(50, 50))
        
        # Acciones barra de herramientas
        accionHeNu = QAction("Nuevo", self)
        accionHeNu.triggered.connect(self.HerNuevo)
        barra_herramientas.addAction(accionHeNu)
        
        accionHeAb = QAction("Abrir", self)
        accionHeAb.triggered.connect(self.HerAbrir)
        barra_herramientas.addAction(accionHeAb)
        
        accionHeGu = QAction("Guardar", self)
        accionHeGu.triggered.connect(self.HerGuardar)
        barra_herramientas.addAction(accionHeGu)
        
        accionHeDe = QAction("Deshacer", self)
        accionHeDe.triggered.connect(self.Deshacer)
        barra_herramientas.addAction(accionHeDe)
        
        accionHeRe = QAction("Rehacer", self)
        accionHeRe.triggered.connect(self.Rehacer)
        barra_herramientas.addAction(accionHeRe)
        
        accionHeCor = QAction("Cortar", self)
        accionHeCor.triggered.connect(self.Cortar)
        barra_herramientas.addAction(accionHeCor)
        
        accionHeCop = QAction("Copiar", self)
        accionHeCop.triggered.connect(self.Copiar)
        barra_herramientas.addAction(accionHeCop)
        
        accionHePe = QAction("Pegar", self)
        accionHePe.triggered.connect(self.Pegar)
        barra_herramientas.addAction(accionHePe)
        
        accionHeBu = QAction("Buscar", self)
        accionHeBu.triggered.connect(self.HerBuscar)
        barra_herramientas.addAction(accionHeBu)
        
        accionHeRee = QAction("Reemplazar", self)
        accionHeRee.triggered.connect(self.HerReemplazar)
        barra_herramientas.addAction(accionHeRee)
        
        accionHeDictar = QAction("Dictar", self)
        accionHeDictar.triggered.connect(self.dictar_por_voz)
        barra_herramientas.addAction(accionHeDictar)
        
        self.addToolBar(barra_herramientas)

    # Funciones menu Editar
    def Deshacer(self):
        self.texto.undo()
    
    def Rehacer(self):
        self.texto.redo()

    def Copiar(self):
        self.texto.copy()

    def Cortar(self):
        self.texto.cut()
    
    def Pegar(self):
        self.texto.paste()

    # Funciones barra herramientas
    def HerNuevo(self):
        self.texto.clear()
        self.archivo_actual = None
        self.mensaje_estado = "Nuevo archivo creado"
        self.actualizar_contador()
    
    def HerAbrir(self):
        archivo, _ = QFileDialog.getOpenFileName(self, "Abrir archivo", "", "Archivos de texto (*.txt);;Todos (*.*)")
        if archivo:
            with open(archivo, "r", encoding="utf-8") as f:
                self.texto.setPlainText(f.read())
            self.archivo_actual = archivo
            self.mensaje_estado = f"Archivo abierto: {archivo}"
            self.actualizar_contador()

    def HerGuardar(self):
        if not self.archivo_actual:
            archivo, _ = QFileDialog.getSaveFileName(self, "Guardar archivo", "", "Archivos de texto (*.txt)")
            if not archivo:
                return
            self.archivo_actual = archivo

        with open(self.archivo_actual, "w", encoding="utf-8") as f:
            f.write(self.texto.toPlainText())
        
        self.mensaje_estado = f"Archivo guardado: {self.archivo_actual}"
        self.actualizar_contador()
                
    def HerDeshacer(self):
        self.texto.undo()
    
    def HerRehacer(self):
        self.texto.redo()
    
    def HerCortar(self):
        self.texto.cut()
    
    def HerCopiar(self):
        self.texto.copy()

    def HerPegar(self):
        self.texto.paste()

    def HerBuscar(self):
        texto_buscar, ok = QInputDialog.getText(self, "Buscar", "Texto a buscar:")
        if ok and texto_buscar:
            cursor = self.texto.textCursor()
            document = self.texto.document()
            found = document.find(texto_buscar, cursor)
            if found.isNull():
                self.mensaje_estado = f"No se encontró '{texto_buscar}'"
            else:
                self.texto.setTextCursor(found)
                self.mensaje_estado = f"Texto '{texto_buscar}' encontrado"
            self.actualizar_contador()
    
    def HerReemplazar(self):
        texto_buscar, ok1 = QInputDialog.getText(self, "Reemplazar", "Texto a buscar:")
        if not ok1 or not texto_buscar:
            return

        texto_reemplazar, ok2 = QInputDialog.getText(self, "Reemplazar", "Reemplazar con:")
        if not ok2:
            return
        
        contenido = self.texto.toPlainText()
        nuevo_contenido = contenido.replace(texto_buscar, texto_reemplazar)
        self.texto.setPlainText(nuevo_contenido)

        self.mensaje_estado = f"Reemplazado '{texto_buscar}' por '{texto_reemplazar}'"
        self.actualizar_contador()

    def actualizar_contador(self):
        texto_actual = self.texto.toPlainText()
        self.widget_contador.update_from_text(texto_actual)
        
        if self.mensaje_estado:
            self.status.showMessage(self.mensaje_estado, 5000)
            self.mensaje_estado = ""
        
    def reconocer_voz(self):
        recognizer = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                self.status.showMessage("Escuchando... (Di 'terminar' para salir)")
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            texto = recognizer.recognize_google(audio, language="es-ES")
            return texto.lower().strip()
            
        except sr.WaitTimeoutError:
            return None 
        except sr.UnknownValueError:
            return None 
        except sr.RequestError:
            self.mensaje_estado = "Error de conexión"
            return "terminar"
        except Exception as e:
            print(f"Error: {e}")
            return None

    def dictar_por_voz(self):
        self.texto.moveCursor(QTextCursor.End)
        self.texto.setFocus()
        
        self.texto.setFontWeight(QFont.Normal)
        self.texto.setFontItalic(False)
        self.texto.setFontUnderline(False)
        
        self.mensaje_estado = "Modo dictado activo. Esperando 5s de silencio para terminar."
        self.actualizar_contador()

        while True:
            QApplication.processEvents()
            
            texto = self.reconocer_voz()
            
            # Si recibimos la señal de timeout, terminamos el dictado
            if texto == "__TIMEOUT__":
                self.status.showMessage("Dictado finalizado por inactividad (5s).")
                break
                
            if texto is None:
                continue
                
            # Comandos de formato
            if "negrita" in texto:
                peso_actual = self.texto.fontWeight()
                nuevo_peso = QFont.Bold if peso_actual != QFont.Bold else QFont.Normal
                self.texto.setFontWeight(nuevo_peso)
                self.status.showMessage("Formato cambiado: Negrita")
                
            elif "cursiva" in texto:
                estado_actual = self.texto.fontItalic()
                self.texto.setFontItalic(not estado_actual)
                self.status.showMessage("Formato cambiado: Cursiva")
                
            elif "subrayado" in texto:
                estado_actual = self.texto.fontUnderline()
                self.texto.setFontUnderline(not estado_actual)
                self.status.showMessage("Formato cambiado: Subrayado")
            
            elif "nuevo documento" in texto:
                self.HerNuevo()
                self.status.showMessage("Nuevo documento creado")
                
            elif "guardar archivo" in texto:
                self.HerGuardar()
                self.status.showMessage("Archivo guardado.")
                # Opcional: break si quieres que al guardar también salga

            else:
                self.texto.insertPlainText(texto + " ")
                
                sb = self.texto.verticalScrollBar()
                sb.setValue(sb.maximum())
                
                # Actualizar el contador widget en tiempo real
                self.actualizar_contador()

        

if __name__ == "__main__":
    app = QApplication([])
    ventana1 = VentanaPrincipal()
    ventana1.show()
    app.exec()
