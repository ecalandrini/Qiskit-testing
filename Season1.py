# -*- coding: utf-8 -*-
"""
Created on Tue Sep 19 15:52:10 2023

@author: ecalandrini
"""

#%%
from qiskit import *
from qiskit.tools.visualization import plot_histogram, plot_bloch_multivector, plot_distribution, array_to_latex

simulator_circuit = Aer.get_backend("qasm_simulator")
simulator_state = Aer.get_backend("statevector_simulator")
simulator_matrix = Aer.get_backend("unitary_simulator")

%matplotlib inline

# define a quantum register with 2 qubits
qr = QuantumRegister(2)
# define a classical register with 2 bits
cr = ClassicalRegister(2)

# define a quantum circuit with the 2 qubits and the 2 bits
circuit = QuantumCircuit(qr, cr)

# apply an hadamard gate on qubit 0
circuit.h(qr[0])

# apply a CNOT gate with control on qubit 0 and target on qubit 1
circuit.cx(qr[0], qr[1])

# measure the qubits and store the results in the classical bits
circuit.measure(qr, cr)
circuit.draw("mpl")

# run the circuit 1024 times and get the statistics
res = execute(circuit, backend=simulator_circuit, shots = 2048).result()
# plot the histogram of the measured states. note that it is in a superposition of the state 00 and 11 with equal probability
plot_distribution(res.get_counts(circuit))

#%%
# define a circuit with 1 qubit and 1 bit
circuit = QuantumCircuit(1, 1)

# calculate the state of the qubit, it is |0>
res = execute(circuit, backend=simulator_state).result()
statevector = res.get_statevector()
# print the state of the qubit, it is |0>
print(statevector)

# represent the state of the qubit on the Bloch sphere
plot_bloch_multivector(statevector)

# apply the X gate (not)
circuit.x(0)
circuit.draw("mpl")

# calculate the state of the qubit, it is |1>
res = execute(circuit, backend=simulator_state).result()
statevector = res.get_statevector()
# print the state of the qubit, it is |1>
print(statevector)

# represent the state of the qubit on the Bloch sphere
plot_bloch_multivector(statevector)

# measure the qubit and store the measurement in the classical bit
circuit.measure([0], [0])
circuit.draw("mpl")

# run the circuit 1024 times and get the statistics
res = execute(circuit, backend=simulator_circuit, shots = 1024).result()
plot_distribution(res.get_counts(circuit))

#%%
circuit = QuantumCircuit(1, 1)
circuit.x(0)
circuit.draw("mpl")

# print the unitary operator describing the circuit
res = execute(circuit, backend=simulator_matrix).result()
unitary = res.get_unitary()
print(unitary)

#%% Quantum teleportation
'''
teleport the qubit 0 to qubit 2
'''

# build a quantum circuit with 3 qubits and 3 bits
circuit = QuantumCircuit(3, 3)

circuit.x(0)
circuit.barrier()

circuit.h(1)
circuit.cx(1,2)

circuit.cx(0,1)
circuit.h(0)

circuit.barrier()
circuit.measure([0,1], [0,1])

circuit.barrier()
circuit.cx(1,2)
circuit.cz(0,2)
circuit.measure(2, 2)
circuit.draw("mpl")

result = execute(circuit, backend=simulator_circuit, shots=1024).result()
counts = result.get_counts()
plot_distribution(counts)

#%% Quantum teleportation 2
'''
teleport the qubit 0 to qubit 2
'''

# build a quantum circuit with 3 qubits and 3 bits
circuit = QuantumCircuit(3, 3)

circuit.h(0)
circuit.barrier()

circuit.h(1)
circuit.cx(1,2)

circuit.cx(0,1)
circuit.h(0)

circuit.barrier()
circuit.measure([0,1], [0,1])

circuit.barrier()
circuit.cx(1,2)
circuit.cz(0,2)
circuit.measure(2, 2)
circuit.draw("mpl")

result = execute(circuit, backend=simulator_circuit, shots=5000).result()
counts = result.get_counts()
plot_distribution(counts)

#%%

secretnumber = '1'

circuit = QuantumCircuit(len(secretnumber)+1, len(secretnumber))

circuit.h(range(len(secretnumber)))
circuit.x(len(secretnumber))
circuit.h(len(secretnumber))

circuit.barrier()

for i, val in enumerate(reversed(secretnumber)):
    if val == '1':
        circuit.cx(i, len(secretnumber))

circuit.barrier()
circuit.h(range(len(secretnumber)))
circuit.measure(range(len(secretnumber)), range(len(secretnumber)))

circuit.draw("mpl")
result = execute(circuit, backend=simulator_circuit, shots=1).result()
counts = result.get_counts()
print(counts)


