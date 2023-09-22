# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 09:40:23 2023

@author: ecalandrini
"""

from qiskit import *
from qiskit.tools.visualization import plot_histogram, plot_bloch_multivector, plot_distribution, array_to_latex

simulator_circuit = Aer.get_backend("qasm_simulator")
simulator_state = Aer.get_backend("statevector_simulator")
simulator_matrix = Aer.get_backend("unitary_simulator")

%matplotlib inline

winner = 7
winner_bit = "{0:b}".format(winner)
Nqubit = len(winner_bit)
magic_string = [j for j,i in enumerate(reversed(winner_bit)) if i == '1']
print(winner, winner_bit, Nqubit)

circuit = QuantumCircuit(Nqubit, Nqubit)

# circuit.x(magic_string)
circuit.x([0,1])
# circuit.barrier()

res = execute(circuit, backend=simulator_state).result()
# counts = res.get_counts()
# plot_distribution(counts)
sv = res.get_statevector()
sv.draw('latex')
print(sv)

if len(magic_string) == 1:
    circuit.z(magic_string[0])
else:
    a=1
    for i in magic_string[1:]:
        if a<0:
            circuit.x(magic_string[0])
        circuit.cz(magic_string[0], i)
        if a<0:
            circuit.x(magic_string[0])
        a *= -1

# circuit.x([1])
# circuit.z(0)
# circuit.barrier()
circuit.measure(range(Nqubit),range(Nqubit))
circuit.draw("mpl")
print(circuit.depth())
res = execute(circuit, backend=simulator_state).result()
# counts = res.get_counts()
# plot_distribution(counts)
sv = res.get_statevector()
sv.draw('latex')
sv.draw('qsphere')
print(sv)
# unitary = res.get_unitary()
# print(unitary)