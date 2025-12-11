import os

from PySide6.QtGui import QAction, QIcon, QKeySequence
from PySide6.QtWidgets import QApplication, QMainWindow, QToolBar, QTextEdit, QInputDialog, QFileDialog
from PySide6.QtCore import Qt, QSize


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
        texto = self.texto.toPlainText()
        palabras = len(texto.split())
        estado = f"{self.mensaje_estado} | Palabras: {palabras}" if self.mensaje_estado else f"Palabras: {palabras}"
        self.status.showMessage(estado, 5000)
        self.mensaje_estado = ""
        

if __name__ == "__main__":
    app = QApplication([])
    ventana1 = VentanaPrincipal()
    ventana1.show()
    app.exec()
