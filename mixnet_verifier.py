from verify import verify
import sys

NET_SIZE = 32


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "Uage: mixnet_verifier.py <keys_file_path> <mixnet_output_file_path>"
        exit()
    try:
        if verify(sys.argv[2], sys.argv[1]):
            print "Verification succeeded"
        else:
            print "Verification failed"

    except Exception, e:
        print "Exception occured:"
        print str(e)
