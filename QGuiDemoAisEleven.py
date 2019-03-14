# --------------------------------------------------------------------------------------------------------------
# Import libraries
# --------------------------------------------------------------------------------------------------------------
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import execute, BasicAer, IBMQ
from qiskit.providers.ibmq import least_busy
from qiskit.tools.monitor import job_monitor, backend_monitor, backend_overview
from qiskit.tools.visualization import plot_state_city, plot_bloch_multivector, plot_state_paulivec, plot_state_hinton, plot_state_qsphere, plot_histogram

import Qconfig
import math
from random import randint

# --------------------------------------------------------------------------------------------------------------
# global variable
# --------------------------------------------------------------------------------------------------------------
Counts = 0
# --------------------------------------------------------------------------------------------------------------
# The function to find period using the Quantum computer
# Input : a and N for which the period is to be computed.
# Output : period r of the function a^x mod N
# --------------------------------------------------------------------------------------------------------------
def period(a, N):
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


    # Run the circuit
    while True:
        global Counts
        Counts = Counts + 1

        # qp.set_api(Qconfig.APItoken, Qconfig.config['url'])  # set the APIToken and API url
        # simulate = qp.execute(["Period_Finding"], backend="ibmqx4", shots=1, timeout=500)
        # IBMQ.enable_account(Qconfig.APItoken, url=Qconfig.config['url'])

        shots = 1  # Number of shots to run the program (experiment); maximum is 8192 shots.
        max_credits = 3  # Maximum number of credits to spend on executions.

        # backend = least_busy(IBMQ.backends(filters=lambda x: not x.configuration().simulator))
        # backend.name()

        backend_sim = BasicAer.get_backend('qasm_simulator')


        # sim_backend = BasicAer.get_backend('qasm_simulator')
        # , shots=shots, max_credits=max_credits
        job = execute(shor, backend_sim).result()
        # job_monitor(job)

        # result = job.result()
        # job.get_counts(shor)
        # backend_overview()
        # print(simulate)
        data = job.get_counts(shor)
        plot_histogram(data)
        # shor.draw(output='mpl', filename='C:\\Users\\mdonovic\\Documents\\Project Map\\tmp\\circuit.jpg')
        # shor.draw(output='text', filename='C:\\Users\\mdonovic\\Documents\\Project Map\\tmp\\circuit.txt')
        # shor.draw(output='text', filename='C:\\Users\\mdonovic\\Documents\\Project Map\\tmp\\circuit.tex')
        print(data)
        plot_histogram(data)
        # print(data)
        data = list(data.keys())
        print("dic data", data)
        r = int(data[0])
        r = 0
        print("quantum data", r)
        l = math.gcd(2 ** 3, r)
        # print(l)
        r = int((2 ** 3) / l)
        print("period", r)
        if (r % 2 == 0) and (((a ** (r / 2)) + 1) %
                             N != 0) and (r != 0) and (r != 8):
            break
    return r


# --------------------------------------------------------------------------------------------------------------
# The main function to compute factors
# Input : The number to be factored, N
# Output : Factors of the number
# --------------------------------------------------------------------------------------------------------------
def Factorize_N(N):
    factors = [0, 0]
    # --------------------------------------------------------------------------------------------------------------
    # Step 1 : Determine the number of bits based on N; n = [log2(N)]
    # --------------------------------------------------------------------------------------------------------------
    n = math.ceil(math.log(N, 2))
    # --------------------------------------------------------------------------------------------------------------
    # Step 2 : Check if N is even. In that case return 2 and the remaining number as factors
    # --------------------------------------------------------------------------------------------------------------
    if N % 2 == 0:
        factors = [2, N / 2]
        return factors
    # --------------------------------------------------------------------------------------------------------------
    # Step 3 : Check if N is of the form P^(k), where P is some prime factor. In that case return P and k.
    # --------------------------------------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------------------------------------
    # Step 4 : Choose a random number between 2...(N-1).
    # --------------------------------------------------------------------------------------------------------------
    # a = randint(2, N - 1)
    a = 11
    # --------------------------------------------------------------------------------------------------------------
    # Step 5 : Take GCD of a and N. t = GCD(a,N)
    # --------------------------------------------------------------------------------------------------------------
    t = math.gcd(N, a)
    if t > 1:
        factors = [t, N / t]
        return factors
    # --------------------------------------------------------------------------------------------------------------
    # Step 6 : t = 1. Hence, no common period. Find Period using Shor's method
    # --------------------------------------------------------------------------------------------------------------
    r = period(a, N)

    # print('r', r)
    # print('a', a)
    # print('l', int(a ** (r / 2) + 1))
    factor_1 = math.gcd(int(a ** (r / 2) + 1), N)
    factor_2 = N / factor_1

    factors = [int(factor_1), int(factor_2)]
    return factors

# --------------------------------------------------------------------------------------------------------------
# Step 0 : Take the input N
# --------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    N = 15
    factors = Factorize_N(N)
    print("The Number being factorized is : 15 with a = 11")
    print("Factors are = ", factors)
    print("Number of times the circuit looped to find out the period = ", Counts)
