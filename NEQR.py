import qiskit as qk
from qiskit import QuantumCircuit
from qiskit import transpile, assemble
from qiskit.tools.jupyter import *
from qiskit.visualization import plot_histogram
import math
import numpy as np
from qiskit import QuantumRegister, ClassicalRegister
import matplotlib.pyplot as mpl

def build_neqr(image: np.ndarray, NEQR_circuit):
    image_size = len(image)
    
    # размер изображения как степень двойки, чтобы определить необходимое количество кубит
    position_num = int(math.log(image_size, 2))
    intensity_num = len(image[0])

    # размер изображения как степень двойки, чтобы определить необходимое количество кубит
    position_num_y = int(math.log(image_size, 2)/2)
    position_num_x = int(math.log(image_size, 2)/2)
    intensity_num = len(image[0])

    # позиция пикселя
    position_value_x = QuantumRegister(position_num_x, "position_value_x")
    position_value_y = QuantumRegister(position_num_y, "position_value_y")
    
    # значение пикселя
    color_value = QuantumRegister(intensity_num, "color_value")
    

    NEQR_circuit.add_register(color_value, position_value_x, position_value_y)
    
    # количество пикселей в схеме
    num_qubits = NEQR_circuit.num_qubits
    
    for position in range(intensity_num):
        NEQR_circuit.i(position)
    # Add Hadamard gates to the pixel positions 

    for position in range(intensity_num, num_qubits):
        NEQR_circuit.h(position)
    NEQR_circuit.barrier()
    
    for n in range(image_size):
        value = format(n, f"0{position_num}b")
        for position, position_value_value in enumerate(value[::-1]):
            if(position_value_value =="0"):
                NEQR_circuit.x(position + intensity_num) 
        for position_1, px_value_1 in enumerate(image[n][::-1]):
            if(px_value_1 == "1"):
                NEQR_circuit.mct([*position_value_x, *position_value_y], color_value[position_1], mode='noancilla')  
        for position, position_value_value in enumerate(value[::-1]):
            if(position_value_value =="0"):
                NEQR_circuit.x(position + intensity_num)                     
        NEQR_circuit.barrier()  
        
    return NEQR_circuit, position_value_x, position_value_y, color_value 
