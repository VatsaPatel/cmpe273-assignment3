import pickle

a = b'\x80\x04\x95<\x00\x00\x00\x00\x00\x00\x00}\x94(\x8c\x04name\x94\x8c\nJohn Smith\x94\x8c\x05email\x94\x8c\x10jsmith@gmail.com\x94\x8c\x03age\x94K\x14u.'

b = b'\x80\x03}q\x00(X\t\x00\x00\x00operationq\x01X\x03\x00\x00\x00PUTq\x02X\x02\x00\x00\x00idq\x03X \x00\x00\x009ad5794ec94345c4873c4e591788743aq\x04X\x07\x00\x00\x00payloadq\x05}q\x06X\x04\x00\x00\x00userq\x07X\x03\x00\x00\x00Fooq\x08su.'

print(pickle.loads(a))