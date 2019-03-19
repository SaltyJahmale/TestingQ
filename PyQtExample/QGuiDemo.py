import math
import random
import sys
import time

# Quantum imports
from qiskit import Aer
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import execute
from qiskit.tools.visualization import plot_histogram
from PyQt5 import QtWidgets, QtGui
from PyQtExample import QGui as MyDialog


class DemoUi(QtWidgets.QMainWindow):
    def __init__(self):
        super(DemoUi, self).__init__()
        self.ui = MyDialog.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.c_button.clicked.connect(self.start_classic)
        self.ui.q_button.clicked.connect(self.start_quantum)
        self.ui.q_input.addItem("2")
        self.ui.q_input.addItem("7")
        self.ui.q_input.addItem("8")
        self.ui.q_input.addItem("11")
        self.ui.q_input.addItem("13")


    def start_classic(self):
        start_time = time.time()

        classic_number_input = self.ui.c_input.text()
        self.shors_algorithm_classical(int(classic_number_input))

        time_diff = time.time() - start_time
        self.ui.c_time_label.setText(str(time_diff))

    def find_period_classical(self, a, N):
        n = 1
        t = a
        while t != 1:
            t *= a
            t %= N
            n += 1
        return n

    def shors_algorithm_classical(self, N):
        x = random.randint(0, N)

        if math.gcd(x, N) != 1:  # step one, pick a number bigger 1 smaller N
            return x, 0, math.gcd(x, N), N / math.gcd(x, N)

        periode = self.find_period_classical(x, N)  # step two find the period (Classical bottleneck)
        while periode % 2 != 0: # step three check if it's an even number otherwise pick another number
            periode = self.find_period_classical(x, N)

        factor_p = math.gcd(x ** int(periode / 2) + 1, N)  # step four compute the factor
        factor_q = math.gcd(x ** int(periode / 2) - 1, N)  # step four compute the factor

        self.ui.c_period_label.setText(str(periode))
        self.ui.c_upper_factor_label.setText(str(factor_p))
        self.ui.c_lower_factor_label.setText(str(factor_q))

    # qc = quantum circuit, qr = quantum register, cr = classical register, a = 2, 7, 8, 11 or 13

    def circuit_a_mod_15(self, qc, qr, cr, a):
        if a == 2:
            qc.cswap(qr[4], qr[3], qr[2])
            qc.cswap(qr[4], qr[2], qr[1])
            qc.cswap(qr[4], qr[1], qr[0])
        elif a == 7:
            qc.cswap(qr[4], qr[1], qr[0])
            qc.cswap(qr[4], qr[2], qr[1])
            qc.cswap(qr[4], qr[3], qr[2])
            qc.cx(qr[4], qr[3])
            qc.cx(qr[4], qr[2])
            qc.cx(qr[4], qr[1])
            qc.cx(qr[4], qr[0])
        elif a == 8:
            qc.cswap(qr[4], qr[1], qr[0])
            qc.cswap(qr[4], qr[2], qr[1])
            qc.cswap(qr[4], qr[3], qr[2])
        elif a == 13:
            qc.cswap(qr[4], qr[3], qr[2])
            qc.cswap(qr[4], qr[2], qr[1])
            qc.cswap(qr[4], qr[1], qr[0])
            qc.cx(qr[4], qr[3])
            qc.cx(qr[4], qr[2])
            qc.cx(qr[4], qr[1])
            qc.cx(qr[4], qr[0])

    # qc = quantum circuit, qr = quantum register, cr = classical register, a = 2, 7, 8, 11 or 13
    def circuit_a_period_15(self, qc, qr, cr, a):
        if a == 11:
            self.circuit_11_period_15(qc, qr, cr)
            return

        # Initialize q[0] to |1>
        qc.x(qr[0])

        # Apply a**4 mod 15
        qc.h(qr[4])
        #   controlled identity on the remaining 4 qubits, which is equivalent to doing nothing
        qc.h(qr[4])
        #   measure
        qc.measure(qr[4], cr[0])
        #   reinitialise q[4] to |0>
        qc.reset(qr[4])

        # Apply a**2 mod 15
        qc.h(qr[4])
        #   controlled unitary
        qc.cx(qr[4], qr[2])
        qc.cx(qr[4], qr[0])
        #   feed forward
        if cr[0] == 1:
            qc.u1(math.pi / 2., qr[4])
        qc.h(qr[4])
        #   measure
        qc.measure(qr[4], cr[1])
        #   reinitialise q[4] to |0>
        qc.reset(qr[4])

        # Apply a mod 15
        qc.h(qr[4])
        #   controlled unitary.
        self.circuit_a_mod_15(qc, qr, cr, a)
        #   feed forward
        if cr[1] == 1:
            qc.u1(math.pi / 2., qr[4])
        if cr[0] == 1:
            qc.u1(math.pi / 4., qr[4])
        qc.h(qr[4])
        #   measure
        qc.measure(qr[4], cr[2])

    def circuit_11_period_15(self, qc, qr, cr):
        # Initialize q[0] to |1>
        qc.x(qr[0])

        # Apply a**4 mod 15
        qc.h(qr[4])
        # controlled identity on the remaining 4 qubits, which is equivalent to doing nothing
        qc.h(qr[4])
        # measure
        qc.measure(qr[4], cr[0])
        # reinitialise q[4] to |0>
        qc.reset(qr[4])

        # Apply a**2 mod 15
        qc.h(qr[4])
        # controlled identity on the remaining 4 qubits, which is equivalent to doing nothing
        # feed forward
        if cr[0] == 1:
            qc.u1(math.pi / 2., qr[4])
        qc.h(qr[4])
        # measure
        qc.measure(qr[4], cr[1])
        # reinitialise q[4] to |0>
        qc.reset(qr[4])

        # Apply 11 mod 15
        qc.h(qr[4])
        # controlled unitary.
        qc.cx(qr[4], qr[3])
        qc.cx(qr[4], qr[1])
        # feed forward
        if cr[1] == 1:
            qc.u1(math.pi / 2., qr[4])
        if cr[0] == 1:
            qc.u1(math.pi / 4., qr[4])
        qc.h(qr[4])
        # measure
        qc.measure(qr[4], cr[2])


    def start_quantum(self):
        start_time = time.time()

        q = QuantumRegister(5, 'q')
        c = ClassicalRegister(5, 'c')
        a = self.ui.q_input.currentText()

        shor = QuantumCircuit(q, c)
        # circuit for a = 7, and plot the results:
        self.circuit_a_period_15(shor, q, c, int(a))
        backend = Aer.get_backend('qasm_simulator')
        sim_job = execute([shor], backend)
        sim_result = sim_job.result()

        sim_data = sim_result.get_counts(shor)
        plot_histogram([sim_data]).show()
        self.ui.q_period_label.setText(str(len(sim_data)))

        time_diff = time.time() - start_time
        self.ui.q_time_label.setText(str(time_diff))

        factor_p = math.gcd(int(self.ui.q_input.currentText()) ** int(len(sim_data) / 2) + 1, 15)  # compute the factor classically
        factor_q = math.gcd(int(self.ui.q_input.currentText()) ** int(len(sim_data) / 2) - 1, 15)  # compute the factor classically

        self.ui.q_upper_factor_label.setText(str(factor_q))
        self.ui.q_lower_factor_label.setText(str(factor_p))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = DemoUi()
    window.setWindowTitle("Quantum Demo")
    window.setWindowIcon(QtGui.QIcon('quantum.png'))
    window.show()
    sys.exit(app.exec_())
