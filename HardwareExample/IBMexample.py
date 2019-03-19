from qiskit.tools.visualization import plot_histogram
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import execute, IBMQ, BasicAer
import math
import Qconfig

q = QuantumRegister(7)
c = ClassicalRegister(3)

# Comment this if run on a simulator
# Account token
# IBMQ.enable_account(Qconfig.APItoken, url=Qconfig.config['url'])

# Comment this if run on a simulator
# Specifically tell to pick this backend
# backend = IBMQ.get_backend('ibmq_16_melbourne')
# print(backend)

# Shor's quantum circuit
shor = QuantumCircuit(q, c)

shor.h(q[0])
shor.h(q[1])
shor.h(q[2])
shor.x(q[6])
shor.cx(q[2], q[4])
shor.cx(q[2], q[5])
shor.cx(q[3], q[5])
shor.ccx(q[1], q[5], q[3])
shor.cx(q[3], q[5])
shor.cx(q[6], q[4])
shor.ccx(q[1], q[4], q[6])
shor.cx(q[6], q[4])
shor.h(q[0])
shor.cu1(math.pi / 2, q[0], q[1])
shor.h(q[1])
shor.cu1(math.pi / 4, q[0], q[2])
shor.cu1(math.pi / 2, q[1], q[2])
shor.h(q[2])
shor.measure(q[0], c[0])
shor.measure(q[1], c[1])
shor.measure(q[2], c[2])

# Execute the quantum circuit on simulator
# Comment this if run on a real device
backend = BasicAer.get_backend('qasm_simulator')
job = execute(shor, backend).result()
data = job.get_counts(shor)
print(data)

plot_histogram(data)