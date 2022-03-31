import sys
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMessageBox

import analizadorLexico as lexico
import analizadorSintactico as sintactico
import analizadorSemantico as semantico


qtCreatorFile = './view/mainView.ui' #Nombre del archivo aquí

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class mainView(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        
        #Titulo de la ventana
        self.setWindowTitle(".:: Analizador Sintáctico::. Segundo Corte - Compiladores e Interpretes - 193282 - 193213")

        #Botones
        self.btnSalir.clicked.connect(self.salir)
        self.btnAnalizar.clicked.connect(self.obtenerDatos)

    #Obtener datos y analizarlos
    def obtenerDatos(self):
        cadena = self.textoEntrada.toPlainText()

        if cadena:

            self.textoEntrada.setStyleSheet('font: 15pt "MS Shell Dlg 2"; color:black;')

            lexico.cadena = cadena
            cadenaReemplazada = self.reemplazarCarateres(lexico.cadena)

            #Metodo analizar
            lexico.analizar(cadenaReemplazada)
            self.textoSalida.clear()

           
            #datos de salida, mostrar en la ventana
            for i in lexico.salidas:

                if str(i[:8]).lower() == "lextoken":
                    # self.textoSalida.appendPlainText(i)
                    self.textoSalida.appendHtml(f'<span style="color: black;">{i}</span>')
                    self.textoSalida.setStyleSheet('font: 15pt "MS Shell Dlg 2"; color:black; background-color: rgb(255, 255, 255);')

                else:
                    self.textoSalida.appendHtml(f'<span style="color: red;"><b>Error Caracter No Válido: &#{int(i[:])};</b></span>')
                    self.textoSalida.setStyleSheet('font: 15pt "MS Shell Dlg 2"; color:black; background-color: rgb(255, 255, 255);')

            self.textoSalida.setStyleSheet('font: 15pt "MS Shell Dlg 2"; color:black; background-color: rgb(255, 255, 255);')
            
            lexico.salidas.clear()
            
            if lexico.error:
                QMessageBox.critical(None, 'Error en analizador lexico', 'Caracter o caracteres no validos')
                self.textoEntrada.setStyleSheet('border: 3px solid red; font: 15pt "MS Shell Dlg 2"; background-color: rgb(255, 255, 255);')
                self.textoSalida.setStyleSheet('border: 3px solid red; font: 15pt "MS Shell Dlg 2"; background-color: rgb(255, 255, 255);')
                print("No pasamos al sintactico")

            else:

                print("Pasamos al sintactico")
                sintactico.ejecucionAlgoritmo(cadenaReemplazada)

                if sintactico.errorSintactico:
                    self.textoSalida.clear()
                    self.textoSalida.appendHtml(f'<span style="color: purple;">ERROR DE SINTAXIS</span>')

                    for i in range(len(sintactico.lista)):
                        self.textoSalida.appendHtml(f'<span style="color: green;">{sintactico.lista[i]}</span>')
                        self.textoSalida.setStyleSheet('font: 15pt "MS Shell Dlg 2"; color:black; background-color: rgb(255, 255, 255);')

                    if len(sintactico.lista) > 0:

                        try:
                            self.textoSalida.appendHtml(f'<span style="color: orange;">ESTO ES EL ERROR: {sintactico.lista[0]} O EL CARACTER QUE ESTA ANTES DE ESTO O FALTA ALGUN CARACTER </span>')
                            self.textoEntrada.setStyleSheet('border: 3px solid red; font: 15pt "MS Shell Dlg 2"; background-color: rgb(255, 255, 255);')
                            self.textoSalida.setStyleSheet('border: 3px solid red; font: 15pt "MS Shell Dlg 2"; background-color: rgb(255, 255, 255);')
                        except:
                            QMessageBox.critical(None, "Error de sintaxis", 'Error de sintaxis, verificar datos!')

                    self.textoEntrada.setStyleSheet('border: 3px solid red; font: 15pt "MS Shell Dlg 2"; background-color: rgb(255, 255, 255);')
                    self.textoSalida.setStyleSheet('border: 3px solid red; font: 15pt "MS Shell Dlg 2"; background-color: rgb(255, 255, 255);')
                    
                    try:
                        QMessageBox.critical(None,"ERROR DE SINTAXIS", f"ERROR DE SINTAXIS: ESTO ES EL ERROR: {sintactico.lista[0]} O EL CARACTER QUE ESTA ANTES DE ESTO O FALTA ALGUN CARACTER")
                    except:
                        QMessageBox.critical(None, "Error de sintaxis", 'Error de sintaxis, verificar datos!')

                else:
                    #LLAMAR SEMANTICO
                    self.textoEntrada.setStyleSheet('border: 3px solid green; font: 15pt "MS Shell Dlg 2"; background-color: rgb(255, 255, 255);')
                    self.textoSalida.setStyleSheet('border: 3px solid green; font: 15pt "MS Shell Dlg 2"; background-color: rgb(255, 255, 255);')
                    QMessageBox.information(None, "Sintaxis Correcta", "Sintaxis Correcto")

                    
                    self.datosSemantico(cadena)

                sintactico.errorSintactico = False
            lexico.error = False 

        else:
            self.textoSalida.clear()
            self.textoEntrada.setStyleSheet('border: 3px solid red; font: 15pt "MS Shell Dlg 2"; background-color: rgb(255, 255, 255);')
            self.textoSalida.setStyleSheet('border: 3px solid gray; font: 15pt "MS Shell Dlg 2"; background-color: rgb(255, 255, 255);')
            QMessageBox.warning(None, 'Campo Vacio','Sin datos de entrada, porfavor ingrese datos')
        
    
    def reemplazarCarateres(self, cadena):
        cadena = list(cadena)
        cadena1 = ''
        for pos,char in enumerate(cadena):
            if(char == "S" and cadena[pos+1] == "t" and cadena[pos+2] == "r" and cadena[pos+3] == "i" and cadena[pos+4] == "n" and cadena[pos+5] == "g"):
                cadena[pos] = cadena[pos].replace("S","s")
            cadena1 += cadena[pos]
            
       
        # cadena1 = ''
        # for i in range(len(cadena)):
        #     if cadena[i] == chr(34):
        #         contador += 1
        #         if contador%2 == 0:
        #             cadena[i] = cadena[i].replace(chr(34), '”')
        #         else:
        #             cadena[i] = cadena[i].replace(chr(34), '“')
        #     cadena1 += cadena[i] 
        return cadena1
    
    def datosSemantico(self, cadena):
        semantico.digramaUML(cadena)

    #Metodo cerrar ventana
    def salir(self):
        salir = QMessageBox.question(self,'Salir','¿Esta seguro/a de salir?', QMessageBox.Yes, QMessageBox.No)
        if salir == QMessageBox.Yes:
            self.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = mainView()
    window.show()
    sys.exit(app.exec_())