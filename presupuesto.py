# Planificador de Presupuesto Mensual - Usamos  PyQt5

from PyQt5.QtGui import QIcon 

import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QDoubleSpinBox, QSpinBox, QComboBox,
    QCheckBox, QPushButton, QTextEdit, QFormLayout, QHBoxLayout, QVBoxLayout,
    QMessageBox, QFileDialog 
)
from PyQt5.QtCore import Qt


# Definir la clase presupuesto

class PresupuestoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Planificador de Presupuesto Mensual")
        self.setMinimumWidth(600)
        self.init_ui()

class PresupuestoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("PresupuestoMensual.png"))
        self.setWindowTitle("Planificador de Presupuesto Mensual")
        self.setMinimumWidth(600)
        self.init_ui() 

    def init_ui(self): 
        # Widgets que son de entrada
        self.title_label = QLabel("<h2>Planificador de Presupuesto Mensual</h2>")
        self.title_label.setAlignment(Qt.AlignCenter)

        # El ingreso mensual
        self.ingreso = QDoubleSpinBox()
        self.ingreso.setPrefix("$ ")
        self.ingreso.setRange(0, 1_000_000_000)
        self.ingreso.setDecimals(2)
        self.ingreso.setValue(500.00)  # Es un valor que se encuentra por defecto

        self.ahorro_percent = QSpinBox()
        self.ahorro_percent.setRange(0, 100)
        self.ahorro_percent.setValue(10)

        self.moneda = QComboBox()
        self.moneda.addItems(["USD",])

        # Principales Categorias
        self.vivienda = QDoubleSpinBox(); self.vivienda.setPrefix("$ "); self.vivienda.setDecimals(2); self.vivienda.setRange(0, 1_000_000_000)
        self.alimentacion = QDoubleSpinBox(); self.alimentacion.setPrefix("$ "); self.alimentacion.setDecimals(2); self.alimentacion.setRange(0, 1_000_000_000)
        self.transporte = QDoubleSpinBox(); self.transporte.setPrefix("$ "); self.transporte.setDecimals(2); self.transporte.setRange(0, 1_000_000_000)
        self.entretenimiento = QDoubleSpinBox(); self.entretenimiento.setPrefix("$ "); self.entretenimiento.setDecimals(2); self.entretenimiento.setRange(0, 1_000_000_000)

        # Deuda (esto es opcional) Inicialmente esta inhabilitado
        self.incluir_deuda = QCheckBox("Incluir pago de deuda")
        self.deuda_monto = QDoubleSpinBox(); self.deuda_monto.setPrefix("$ "); self.deuda_monto.setDecimals(2); self.deuda_monto.setRange(0, 1_000_000_000)
        self.deuda_monto.setEnabled(False) 

        self.btn_calcular = QPushButton("Calcular presupuesto")
        self.btn_limpiar = QPushButton("Limpiar")
        self.btn_guardar = QPushButton("Guardar resumen (.txt)")

        self.resultado = QTextEdit()
        self.resultado.setReadOnly(True)

        # Uso del los Layouts
        form = QFormLayout()
        form.addRow("Ingreso mensual:", self.ingreso)
        form.addRow("Ahorro deseado (%):", self.ahorro_percent)
        form.addRow("Moneda:", self.moneda)
        form.addRow("Vivienda:", self.vivienda)
        form.addRow("Alimentación:", self.alimentacion)
        form.addRow("Transporte:", self.transporte)
        form.addRow("Entretenimiento:", self.entretenimiento)
        form.addRow(self.incluir_deuda, self.deuda_monto)

        botones_layout = QHBoxLayout()
        botones_layout.addWidget(self.btn_calcular)
        botones_layout.addWidget(self.btn_limpiar)
        botones_layout.addWidget(self.btn_guardar)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.title_label)
        main_layout.addLayout(form)
        main_layout.addLayout(botones_layout)
        main_layout.addWidget(QLabel("Resumen:"))
        main_layout.addWidget(self.resultado)

        self.setLayout(main_layout)

        # Uso de las conexiones 
        
        self.incluir_deuda.stateChanged.connect(self.toggle_deuda)
        self.btn_calcular.clicked.connect(self.calcular_presupuesto)
        self.btn_limpiar.clicked.connect(self.limpiar_campos)
        self.btn_guardar.clicked.connect(self.guardar_resumen)

    def toggle_deuda(self, state):
        """Habilita o deshabilita el campo de monto de deuda según checkbox."""
        self.deuda_monto.setEnabled(state == Qt.Checked)

    def calcular_presupuesto(self):
        """Lee entradas, calcula totales y muestra un resumen."""
        ingreso = float(self.ingreso.value())
        if ingreso <= 0:
            QMessageBox.warning(self, "Ingreso inválido", "Ingresa un valor de ingreso mayor a 0.")
            return

        ahorro_pct = int(self.ahorro_percent.value())
        ahorro_amount = ingreso * (ahorro_pct / 100.0)

        # Montos por  cada categoría
        v = float(self.vivienda.value())
        a = float(self.alimentacion.value())
        t = float(self.transporte.value())
        e = float(self.entretenimiento.value())

        deuda = float(self.deuda_monto.value()) if self.incluir_deuda.isChecked() else 0.0

        total_gastos = v + a + t + e + deuda
        restante = ingreso - (ahorro_amount + total_gastos)

        # Construcción del texto el cual da el resultado
        texto = []
        texto.append(f"Ingreso mensual: {self.moneda.currentText()} {ingreso:,.2f}")
        texto.append(f"Ahorro deseado: {ahorro_pct}% → {self.moneda.currentText()} {ahorro_amount:,.2f}")
        texto.append("")
        texto.append("Asignación por categorías:")
        texto.append(f"  - Vivienda: {self.moneda.currentText()} {v:,.2f}")
        texto.append(f"  - Alimentación: {self.moneda.currentText()} {a:,.2f}")
        texto.append(f"  - Transporte: {self.moneda.currentText()} {t:,.2f}")
        texto.append(f"  - Entretenimiento: {self.moneda.currentText()} {e:,.2f}")
        if self.incluir_deuda.isChecked():
            texto.append(f"  - Pago de deuda: {self.moneda.currentText()} {deuda:,.2f}")

        texto.append("")
        texto.append(f"Total gastos (incluye deuda si aplica): {self.moneda.currentText()} {total_gastos:,.2f}")
        texto.append(f"Saldo después de ahorro y gastos: {self.moneda.currentText()} {restante:,.2f}")

        if restante < 0:
            texto.append("\n **Déficit**: estás gastando más de tu ingreso después de ahorrar.")
            texto.append("Sugerencia: reduce gastos o baja el % de ahorro.")
        else:
            texto.append("\n Presupuesto balanceado. Puedes ahorrar y aún te sobra: "
                         f"{self.moneda.currentText()} {restante:,.2f}")

        # Muestra la información en  QTextEdit
        self.resultado.setPlainText("\n".join(texto))

    def limpiar_campos(self):
        """Restablece valores por defecto."""
        self.ingreso.setValue(500.00)
        self.ahorro_percent.setValue(10)
        self.moneda.setCurrentIndex(0)
        self.vivienda.setValue(0.0)
        self.alimentacion.setValue(0.0)
        self.transporte.setValue(0.0)
        self.entretenimiento.setValue(0.0)
        self.incluir_deuda.setChecked(False)
        self.deuda_monto.setValue(0.0)
        self.resultado.clear()

    def guardar_resumen(self):
        """Permite guardar el texto del resumen a un archivo .txt"""
        contenido = self.resultado.toPlainText()
        if not contenido.strip():
            QMessageBox.information(self, "Nada para guardar", "Calcula el presupuesto antes de guardar.")
            return
       # Cuadro de diálogo para guardar el archivo
        fn, _ = QFileDialog.getSaveFileName(self, "Guardar resumen", "resumen_presupuesto.txt", "Text files (*.txt)")
        if fn:
            try:
                with open(fn, "w", encoding="utf-8") as f:
                    f.write(contenido)
                QMessageBox.information(self, "Guardado", f"Resumen guardado en:\n{fn}")
            except Exception as ex:
                QMessageBox.critical(self, "Error al guardar", str(ex))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = PresupuestoApp()
    ventana.show()
    sys.exit(app.exec_())
