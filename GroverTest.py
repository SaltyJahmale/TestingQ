from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import execute, register
from qiskit import IBMQ, Aer
from qiskit.tools.visualization import plot_histogram, circuit_drawer

# Q and C registers
q = QuantumRegister(5)
c = ClassicalRegister(5)

# Build the circuit
qc = QuantumCircuit(q, c)

# Oracle
qc.h(q[1])
qc.h(q[2])
qc.h(q[2])
qc.cx(q[1], q[2])
qc.h(q[2])

# Grover search
qc.h(q[1])
qc.h(q[2])
qc.x(q[1])
qc.x(q[2])
qc.h(q[2])
qc.cx(q[1], q[2])
qc.h(q[2])
qc.x(q[1])
qc.x(q[2])
qc.h(q[1])
qc.h(q[2])

# Measure 
qc.measure(q, c)

# Simulate
results = execute(qc, "qasm_simulator", shots=1000).result()

# Plot the result
plot_histogram(results.get_counts(qc))
