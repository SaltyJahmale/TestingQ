import math
import random
import sys
import time

# Quantum imports
from qiskit import Aer
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import execute
from qiskit.tools.visualization import plot_histogram

# qc = quantum circuit, qr = quantum register, cr = classical register, a = 2, 7, 8, 11 or 13
def circuit_a_mod_15(qc, qr, cr, a):
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
def circuit_a_period_15(qc, qr, cr, a):
    if a == 11:
        circuit_11_period_15(qc, qr, cr)
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
    circuit_a_mod_15(qc, qr, cr, a)
    #   feed forward
    if cr[1] == 1:
        qc.u1(math.pi / 2., qr[4])
    if cr[0] == 1:
        qc.u1(math.pi / 4., qr[4])
    qc.h(qr[4])
    #   measure
    qc.measure(qr[4], cr[2])


def circuit_11_period_15(qc, qr, cr):
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


if __name__ == '__main__':
    q = QuantumRegister(5, 'q')
    c = ClassicalRegister(5, 'c')

    shor = QuantumCircuit(q, c)
    a = 7
    circuit_a_period_15(shor, q, c, int(a))
    backend = Aer.get_backend('qasm_simulator')
    sim_job = execute([shor], backend)
    sim_result = sim_job.result()


    factor_p = math.gcd(int(self.ui.q_input.currentText()) ** int(len(sim_data) / 2) + 1,
                        15)  # compute the factor classically
    factor_q = math.gcd(int(self.ui.q_input.currentText()) ** int(len(sim_data) / 2) - 1,
                        15)  # compute the factor classically

