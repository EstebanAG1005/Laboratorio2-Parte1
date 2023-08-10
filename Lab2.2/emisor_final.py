import socket
import random
import zlib
import matplotlib.pyplot as plt


def string_to_binary(input_string):
    return "".join(format(ord(char), "08b") for char in input_string)


def apply_noise(binary_data, error_probability):
    return "".join(
        bit if random.random() > error_probability else ("1" if bit == "0" else "0")
        for bit in binary_data
    )


def generate_crc(binary_message):
    byte_message = int(binary_message, 2).to_bytes(
        (len(binary_message) + 7) // 8, byteorder="big"
    )
    crc = zlib.crc32(byte_message)
    return format(crc, "032b")


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
    print("Message sent.")


def generate_random_message(size):
    return "".join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(size))


def run_test(message, error_prob, algorithm_choice):
    binary_message = string_to_binary(message)
    algorithm_indicator = "0" if algorithm_choice == "crc" else "1"
    processed_message = algorithm_indicator + (
        generate_crc(binary_message)
        if algorithm_choice == "crc"
        else hamming_encode(binary_message)
    )
    # noisy_message = apply_noise(processed_message, error_prob)
    # send_message(processed_message)
    # In a real-world test, you would need to receive and verify the message here
    # Returning True for simulation purposes
    return True

def run_tests():
    # Establecer tamaños de mensaje más grandes para pruebas extensas.
    message_sizes = [10_000, 50_000, 100_000, 500_000, 1_000_000]
    error_probabilities = [0.01, 0.05, 0.1, 0.15, 0.2]
    algorithm_choices = ["crc", "hamming"]

    results = []

    for size in message_sizes:
        for error_prob in error_probabilities:
            for algorithm_choice in algorithm_choices:
                message = generate_random_message(size)
                success = modified_run_test(message, error_prob, algorithm_choice)
                results.append((size, error_prob, success, algorithm_choice))

    analyze_and_plot(results)

def analyze_and_plot(results):
    message_sizes = sorted(set(x[0] for x in results))
    error_probabilities = sorted(set(x[1] for x in results))

    for algorithm_choice in ["crc", "hamming"]:
        for error_prob in error_probabilities:
            success_rates = [
                sum(1 for x in results if x[1] == error_prob and x[3] == algorithm_choice and x[2] is True) / len([x for x in results if x[1] == error_prob and x[3] == algorithm_choice]) * 100
                for size in message_sizes
            ]
            plt.plot(
                message_sizes,
                success_rates,
                label=f"{algorithm_choice.upper()} Error Probability {error_prob}",
            )

    plt.xlabel("Message Size")
    plt.ylabel("Success Rate (%)")
    plt.legend()
    plt.show()

def send_data_to_receptor(data, host="localhost", port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(data.encode())
        print("Message sent to receptor")


def modified_run_test(message, error_prob, algorithm_choice, port=12345):
    binary_message = string_to_binary(message)
    algorithm_indicator = "0" if algorithm_choice == "crc" else "1"
    processed_message = algorithm_indicator + (
        generate_crc(binary_message)
        if algorithm_choice == "crc"
        else hamming_encode(binary_message)
    )
    noisy_message = apply_noise(processed_message, error_prob)
    
    # Sending the noisy message
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1", port))
    s.sendall(noisy_message.encode("utf-8"))
    response = s.recv(1024)  # Assuming the response will be small, so 1024 bytes should be enough
    s.close()
    
    # The receptor should send back a simple "success" or "failure" string
    if response.decode("utf-8") == "success":
        return True
    else:
        return False

# El punto de entrada principal debe ejecutar las pruebas
if __name__ == "__main__":
    run_tests()



def automated_tests():
    message_sizes = [10_000, 50_000, 100_000, 500_000, 1_000_000]
    error_probabilities = [0.01, 0.05, 0.1]
    algorithm_choices = ["crc", "hamming"]

    results = []

    for size in message_sizes:
        for error_prob in error_probabilities:
            for algorithm_choice in algorithm_choices:
                message = generate_random_message(size)
                success = modified_run_test(message, error_prob, algorithm_choice)
                results.append((size, error_prob, success, algorithm_choice))

    return results


# Uncomment the following lines to send a single message
#message = input("Enter the message: ")
#algorithm_choice = input("Select algorithm (CRC or Hamming): ").strip().lower()
# algorithm_choice = "hamming"
# binary_message = string_to_binary(message)
# algorithm_indicator = "0" if algorithm_choice == "crc" else "1"
# processed_message = algorithm_indicator + (
#     generate_crc(binary_message)
#     if algorithm_choice == "crc"
#     else hamming_encode(binary_message)
# )
# noisy_message = apply_noise(processed_message, 0.01)  # 1% error probability
#send_message(processed_message)

# Uncomment the following line to run the tests
# run_tests()

