mensaje = "Hola Mundo"
mensaje_binario = " ".join(format(ord(i), "08b") for i in mensaje)
print(mensaje_binario)
