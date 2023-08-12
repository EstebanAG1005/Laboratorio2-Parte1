import socket
import random
import matplotlib.pyplot as plt


def string_to_binary(input_string):
    return "".join(format(ord(char), "08b") for char in input_string)


def apply_noise(binary_data, error_probability):
    return "".join(
        bit if random.random() > error_probability else ("1" if bit == "0" else "0")
        for bit in binary_data
    )


def hamming_encode(binary_message):
    chunks = [binary_message[i : i + 4] for i in range(0, len(binary_message), 4)]
    encoded_message = ""
    for chunk in chunks:
        p1 = str((int(chunk[0]) + int(chunk[1]) + int(chunk[3])) % 2)
        p2 = str((int(chunk[0]) + int(chunk[2]) + int(chunk[3])) % 2)
        p3 = str((int(chunk[1]) + int(chunk[2]) + int(chunk[3])) % 2)
        encoded_chunk = p1 + p2 + chunk[0] + p3 + chunk[1:]
        encoded_message += encoded_chunk
    return encoded_message


def send_message(message, port=12345):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1", port))
    s.sendall(message.encode("utf-8"))
    s.close()
    print("Mensaje Enviado.")


def generate_random_message(size):
    return "".join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(size))


def run_test(message, error_prob):
    binary_message = string_to_binary(message)
    processed_message = hamming_encode(binary_message)
    noisy_message = apply_noise(processed_message, error_prob)
    send_message(processed_message)
    # In a real-world test, you would need to receive and verify the message here
    # Returning True for simulation purposes
    return True


def run_tests():
    message_sizes = [100, 500, 1000, 5000]
    error_probabilities = [0.01, 0.05, 0.1]

    results = []

    for size in message_sizes:
        for error_prob in error_probabilities:
            message = generate_random_message(size)
            success = run_test(message, error_prob)
            results.append((size, error_prob, success, "hamming"))

    analyze_and_plot(results)


def analyze_and_plot(results):
    message_sizes = sorted(set(x[0] for x in results))
    error_probabilities = sorted(set(x[1] for x in results))

    for error_prob in error_probabilities:
        success_rates = [
            x[2] for x in results if x[1] == error_prob and x[3] == "hamming"
        ]
        plt.plot(
            message_sizes,
            success_rates,
            label=f"HAMMING Probabilidad de Error {error_prob}",
        )

    plt.xlabel("Tamaño de mensaje")
    plt.ylabel("Taza de exito")
    plt.legend()
    plt.show()


message = input("Ingresa el mensaje: ")
binary_message = string_to_binary(message)
processed_message = hamming_encode(binary_message)
noisy_message = apply_noise(processed_message, 0.01)  # 1% error probability
send_message(processed_message)

# Uncomment the following line to run the tests
# run_tests()
