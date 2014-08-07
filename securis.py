"""
Securis.py

command line encrypted tcp chat line
software developed by Joe Dolan
"""

"""import statements"""
#Cryptography scripts
from Crypto import Random
from Crypto.Cipher import AES
import base64

#networking scripts
import socket
import select


#UI scripts

cypher = '1333333333333337' #default cypher to use as placeholder.

#Introduction to the program

BS = 16 #block size in bytes
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS) #encryption algorithm
unpad = lambda s: s[0:-ord(s[-1])] #decryption algorithm


#AES cypher creation class. Makes it super easy to use
class AESCipher:
    def __init__(self, key):
        self.key = key

    def encrypt(self, raw):
        raw = pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(enc[16:]))

#initialization function
def intro():
    cyphertext = raw_input("Please enter the text cypher (length must be multiple of 8): ")

    #if it's actually a multiple of 8
    if( len(cyphertext) % 16 == 0 ):
        print("Cypher creation Successful.")

        username = raw_input("What do you want your handle to be?: ")

        cypher = AESCipher(cyphertext)

        #enter main loop
        while(True):
            message = raw_input(">> ")
            encoded = cypher.encrypt(message)
            decoded = cypher.decrypt(encoded)
            print "%s: [%s], [%s]" % (username, encoded, decoded)

    #if they're an idiot
    else:
        print("Error, not a multiple of 8!")
        intro()
"""
if __name__ == "__main__":
    CONNECTED_LIST = []
    RECV_BUFFER = 4096
    PORT = 1337

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", PORT))
    server_socket.listen(10)

    CONNECTED_LIST.append(server_socket)

    print("Chat server connected on port" + str(PORT))

    read_sockets, write_sockets, error_sockets = select.select(CONNECTED_LIST,[], [])

    while True:
        for sock in read_sockets:
            #new connection
            if(sock == server_socket):
                sockfd, addr = server_socket.accept()
                CONNECTED_LIST.append(sockfd)

    server_socket.close()
"""
intro()