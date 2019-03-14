from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import execute, BasicAer, IBMQ
import math
import Qconfig


# Create the first Quantum Register called "qr" with 5 qubits
qr = QuantumRegister(5, 'qr')

# Create your first Classical Register  called "cr" with 3 bits
cr = ClassicalRegister(3, 'cr')

# Create the first QuantumProgram object instance called shor.
shor = QuantumCircuit(qr, cr, name='Period_Finding')

# Create the circuit for period finding
# Initialize qr[0] to |1> and create a superposition on the top 8 qubits
shor.x(qr[0])

# Step one : apply 11**4 mod 15
shor.h(qr[2])

# Controlled Identity to remaining gates which is equivalent to doing nothing
shor.h(qr[2])
shor.measure(qr[2], cr[0])

# Reinitialize to |0>
shor.reset(qr[2])

# Step two : apply 11**2 mod 15
shor.h(qr[2])

# Controlled Identity to remaining gates which is equivalent to doing nothing
if cr[0] == 1:
    shor.u1(math.pi / 2.0, qr[2])
    shor.h(qr[2])
shor.measure(qr[2], cr[1])

# Reinitialize to |0>
shor.reset(qr[2])

# Step three : apply 11 mod 15
shor.h(qr[2])

# Controlled not gates in between to remaining gates which is equivalent to doing nothing
shor.cx(qr[2], qr[1])
shor.cx(qr[2], qr[4])

# Feed forward and measure
if cr[1] == 1:
    shor.u1(math.pi / 2.0, qr[2])
if cr[0] == 1:
    shor.u1(math.pi / 4.0, qr[2])
shor.h(qr[2])
shor.measure(qr[2], cr[2])

# IBMQ.enable_account(Qconfig.APItoken, url=Qconfig.config['url'])

# backend = least_busy(IBMQ.backends(filters=lambda x: not x.configuration().simulator))
# backend.name()

# Testing with simulator works
backend = BasicAer.get_backend('qasm_simulator')


# Error: 'Invalid job state. The job should be DONE but it is JobStatus.ERROR'
job = execute(shor, backend).result()
data = job.get_counts(shor)

print(data)