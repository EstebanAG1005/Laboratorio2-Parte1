def calcularParidad(bits, r):
    n = len(bits)
    res = 0
    for i in range(n):
        if bits[i] == '1' and (i & (1 << (r - 1))) != 0:
            res = res ^ 1
    return res

def hammingCodificar(data):
    paridad_bits = [0] * 4
    paridad_bits[0] = data[0] ^ data[1] ^ data[3] # Paridad para las posiciones 3, 5, 7
    paridad_bits[1] = data[0] ^ data[2] ^ data[3] # Paridad para las posiciones 3, 6, 7
    paridad_bits[2] = data[1] ^ data[2] ^ data[3] # Paridad para las posiciones 5, 6, 7
    return [paridad_bits[0], paridad_bits[1], data[0], paridad_bits[2], data[1], data[2], data[3]]

data = "0110"  # Solo 4 bits de datos
print("Mensaje original:", data)
data = [int(b) for b in data]
codeword = hammingCodificar(data)
codeword_str = "".join(map(str, codeword))
print("Codeword Hamming:", codeword_str)

# Escribir el mensaje codificado en el archivo output2.txt
with open('output2.txt', 'w') as file:
    file.write(codeword_str)
