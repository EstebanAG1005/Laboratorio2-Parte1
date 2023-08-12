import socket
import zlib
import random
import matplotlib.pyplot as plt
import time

HOST = "127.0.0.1"
PORT = 65432


def generate_crc(input_string):
    return format(zlib.crc32(input_string.encode()), "02x")


def string_to_binary(input_string):
    return "".join(format(ord(char), "08b") for char in input_string)


def run_test(message_length, number_of_tests):
    success_count = 0

    for _ in range(number_of_tests):
        test_string = "".join(
            random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
            for _ in range(message_length)
        )
        binary_data = string_to_binary(test_string)
        crc_data = binary_data + generate_crc(
            binary_data
        )  # Combina los datos en binario con el CRC

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(crc_data.encode())
            response = s.recv(1024)

            if response.decode() == "SUCCESS":
                success_count += 1

        time.sleep(0.1)  # Agrega una pausa de 0.1 segundos entre intentos

    return success_count


def manual_mode():
    input_string = input("Ingrese el texto a enviar: ")
    binary_data = string_to_binary(input_string)
    crc_data = binary_data + generate_crc(
        binary_data
    )  # Combina los datos en binario con el CRC

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(crc_data.encode())


def automated_tests():
    test_lengths = [10, 50, 100, 500, 1000]
    number_of_tests = 10000
    success_rates = []

    for length in test_lengths:
        success_count = run_test(length, number_of_tests)
        success_rate = (success_count / number_of_tests) * 100
        success_rates.append(success_rate)

    plt.plot(test_lengths, success_rates, "-o")
    plt.xlabel("Length of Message")
    plt.ylabel("Success Rate (%)")
    plt.title(f"Success Rate over {number_of_tests} tests for varying message lengths")
    plt.show()


def main():
    mode = input("Choose mode (manual/automated): ")

    if mode == "manual":
        manual_mode()
    elif mode == "automated":
        automated_tests()
    else:
        print("Invalid mode selected.")


if __name__ == "__main__":
    main()
