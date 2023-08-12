import socket
import zlib

def generate_crc(input_string):
    return format(zlib.crc32(input_string.encode()), "02x")

def append_crc(input_string, crc):
    return input_string + crc

def main():
    input_string = input("Ingrese el texto a enviar: ")
    crc = generate_crc(input_string)
    output_string = append_crc(input_string, crc)

    # Crear un socket cliente
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 12345))
    client_socket.send(output_string.encode())
    client_socket.close()

    print("Texto con CRC enviado")

if __name__ == "__main__":
    main()
