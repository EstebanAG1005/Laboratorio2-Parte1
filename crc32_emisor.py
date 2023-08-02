import zlib
import os


def generate_crc(input_string):
    return format(zlib.crc32(input_string.encode()), "02x")


def append_crc(input_string, crc):
    return input_string + crc


def main():
    input_string = input("Ingrese el texto a enviar: ")
    crc = generate_crc(input_string)
    output_string = append_crc(input_string, crc)

    with open("output.txt", "w") as f:
        f.write(output_string)

    print("Texto con CRC guardado en output.txt")


if __name__ == "__main__":
    main()
