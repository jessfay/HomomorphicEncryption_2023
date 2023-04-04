from phe import paillier
import json
import socket
def server_program():
    host = socket.gethostname()
    port = 5500 
   
    server_socket = socket.socket()  
    server_socket.bind((host, port)) 
    server_socket.listen(2)
    conn, address = server_socket.accept() 
    print("Connection from: " + str(address))
    while True:
        data = conn.recv(50000).decode()
        received_dict = json.loads(data)
        pk = received_dict['public_key']
        n=int(pk['n'])
        public_key_rec = paillier.PaillierPublicKey(n)
        enc_nums_rec = [
        paillier.EncryptedNumber(public_key_rec, int(x[0]), int(x[1]))                                                                                                                 
        for x in received_dict['value']
        ]
        encrypted_number_list= (enc_nums_rec[0], enc_nums_rec[1],enc_nums_rec[2])     
        x1 = 2
        x2 = 4
        x3 = 6
        y = (encrypted_number_list[0] * x1) + (encrypted_number_list[1] * x2) + (encrypted_number_list[2] * x3)                       
        encrypted_value_list = [y]
        enc_with_one_pub_key = {}
        enc_with_one_pub_key['public_key'] = {'g': public_key_rec.g, 'n': public_key_rec.n}
        enc_with_one_pub_key['value'] = [
        (str(y.ciphertext()), y.exponent) for y in encrypted_value_list 
        ]
        serialized = json.dumps(enc_with_one_pub_key)
        if not data:
            break
        print("from connected user: " + str(data))
        conn.send(serialized.encode()) 
       


server_program()


