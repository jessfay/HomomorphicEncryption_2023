from phe import paillier
import json

public_key, private_key = paillier.generate_paillier_keypair()



secret_number_list = [3, 5, 7]
encrypted_number_list = [public_key.encrypt(x) for x in secret_number_list]


enc_with_one_pub_key = {}
enc_with_one_pub_key['public_key'] = {'g': public_key.g, 'n': public_key.n}
enc_with_one_pub_key['value'] = [
	(str(x.ciphertext()), x.exponent) for x in encrypted_number_list 
]
serialized = json.dumps(enc_with_one_pub_key)


import socket


def client_program():
    host = socket.gethostname()  
    port = 5500
    client_socket = socket.socket()  
    client_socket.connect((host, port)) 
    message = serialized 
    while message.lower().strip() != 'bye':
        client_socket.send(message.encode())  
        data = client_socket.recv(50000).decode()  
        print('Received from server: ' + data)  
        received_dict = json.loads(data)
        y = received_dict['value']
        enc_nums_rec = [
        paillier.EncryptedNumber(public_key, int(y[0][0]), int(y[0][1]))
        ]
        v = private_key.decrypt(enc_nums_rec[0])
        print(v)
        message = input(" -> ")
        client_socket.close()


client_program()

