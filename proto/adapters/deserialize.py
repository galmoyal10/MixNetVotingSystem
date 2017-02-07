from proto.proto_files.concrete_crypto_pb2 import ElGamalCiphertext
from proto.proto_files.crypto_pb2 import RerandomizableEncryptedMessage
from proto.proto_files.mixing_pb2 import MixBatchHeader
from proto.proto_files.mixing_pb2 import Mix2Proof
from google.protobuf.internal import decoder


def deserialize_message_from_buffer(buffer, current_position, message_type):
    message_size, message_position = decoder._DecodeVarint(buffer, current_position)
    message = message_type()
    message.ParseFromString(buffer[message_position:message_position + message_size])
    return message, message_position + message_size


def deserialize_messages_list(buffer, num_of_messages, current_pos, message_type):
    messages = list()
    for m_index in xrange(0, num_of_messages):
        message, current_pos = deserialize_message_from_buffer(buffer, current_pos, message_type)
        messages.append(message)
    return messages, current_pos


def deserialize_mixnet_output_from_file(file_path):
    ciphers = list()
    proofs = list()
    with open(file_path, "rb") as input_file:
        messages_buffer = input_file.read()
    current_pos = 0
    header, current_pos = deserialize_message_from_buffer(messages_buffer, current_pos, MixBatchHeader)
    for layer in xrange(0, header.layers + 1):
        ciphers_of_layer = list()
        raw_ciphers, current_pos = deserialize_messages_list(messages_buffer, 2 ** header.logN, current_pos, RerandomizableEncryptedMessage)
        for raw_cipher in raw_ciphers:
            cipher = ElGamalCiphertext()
            cipher.ParseFromString(raw_cipher.data)
            ciphers_of_layer.append(cipher)
        ciphers.append(ciphers_of_layer)
    for layer in xrange(0, header.layers):
        proofs_of_layer, current_pos = deserialize_messages_list(messages_buffer, 2 ** (header.logN - 1), current_pos, Mix2Proof)
        proofs.append(proofs_of_layer)
    return header, ciphers, proofs


def deserialize_from_file(file_path, message_type, header_exist = False):
    messages = list()
    with open(file_path, "rb") as input_file:
        messages_buffer = input_file.read()
    current_pos = 0
    if header_exist:
        header, current_pos = deserialize_message_from_buffer(messages_buffer, current_pos, MixBatchHeader)
        messages.append(header)
    while current_pos != len(messages_buffer):
        message, current_pos = deserialize_message_from_buffer(messages_buffer, current_pos, message_type)
        messages.append(message)
    return messages
