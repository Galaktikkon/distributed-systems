import socket

server_ip = "127.0.0.1"
java_port = 9008
python_port = 9009
msg = "Ping Python Udp!"

print("PYTHON UDP CLIENT")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# exercise 0

# print("Sending Ping to Server...")
# client_socket.sendto(bytes(msg, "cp1250"), (server_ip, java_port))

# exercise 2

# buff, (ip, port) = client_socket.recvfrom(1024)
# print(f"Received message: {buff.decode()}, from /{ip}:{port}")

# exercise 3

msg_bytes = (300).to_bytes(4, byteorder="little")

print("Sending little endian...")
client_socket.sendto(msg_bytes, (server_ip, java_port))

print("Listening for 301 response")
buff, (ip, port) = client_socket.recvfrom(1024)

response_number = int.from_bytes(buff, byteorder="big")
print(f"Received message: {response_number}, from /{ip}:{port}")
