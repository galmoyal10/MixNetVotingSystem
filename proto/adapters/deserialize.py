from proto.proto_files.concrete_crypto_pb2 import ElGamalCiphertext
from proto.proto_files.crypto_pb2 import RerandomizableEncryptedMessage
from proto.proto_files.mixing_pb2 import MixBatchHeader
from proto.proto_files.mixing_pb2 import Mix2Proof
from google.protobuf.internal import decoder

# Utility functions for protobuf reading #


class DeserializationException(Exception):
    def __init__(self, file_path):
        super(DeserializationException, self).__init__("could not read protobuf message from " + file_path)


def deserialize_message_from_buffer(buffer, current_position, message_type):
    """
    reads a single message from a buffer
    :param buffer: the buffer to read from
    :param current_position: the position in the buffer which the message is in
    :param message_type: the Proto message type to attempt to read
    :return: the deserialized message and the first index in the buffer beyond the message
    """
    message_size, message_position = decoder._DecodeVarint(buffer, current_position)
    message = message_type()
    message.ParseFromString(buffer[message_position:message_position + message_size])
    return message, message_position + message_size


def deserialize_messages_list(buffer, num_of_messages, current_pos, message_type):
    """
    deserializes a list of messages from a buffer
    (python protobuf does not support parseDelimitedFrom...)
    :param buffer: the buffer to read from
    :param num_of_messages: the number of serialized messages that the buffer contains
    :param current_pos: current position in the buffer
    :param message_type: the Proto message type to attempt to read
    :return: a list of deserialized messages and the first index in the buffer beyond the messages list
    """
    messages = list()
    for m_index in xrange(0, num_of_messages):
        message, current_pos = deserialize_message_from_buffer(buffer, current_pos, message_type)
        messages.append(message)
    return messages, current_pos


def deserialize_mixnet_output_from_file(file_path):
    """
    Deserialize a complete mixnet output file as given when
    running the mixer.jar with: "mixer.jar -k ecelgamal.key -i outfile.enc -o mixed.enc"
    :param file_path: the path of the output file to read from
    :return: a MixBatchHeader message, a list of ElGamalCiphertext messages and a list of Mix2Proof messages
    """
    try:
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
    except Exception:
        raise DeserializationException(file_path)


def deserialize_from_file(file_path, message_type):
    """
    deserialize a list of messages from a file
    :param file_path: the path of the file to read from
    :param message_type: the Proto message type that was serialized in the file
    :return: a list of messages
    """
    try:
        messages = list()
        with open(file_path, "rb") as input_file:
            messages_buffer = input_file.read()
        current_pos = 0
        while current_pos != len(messages_buffer):
            message, current_pos = deserialize_message_from_buffer(messages_buffer, current_pos, message_type)
            messages.append(message)
        return messages
    except Exception:
        raise DeserializationException(file_path)
