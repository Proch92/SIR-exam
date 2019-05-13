from network import Network
import sys
import glob

RAND_IN = 2
RAND_OUT = 2
RAND_SIZE = 50


def main():
    filename = None
    net = Network()

    if len(sys.argv) > 0:
        filename = sys.argv[1]
    else:
        filename = "test.net"

    if glob.glob(filename):
        net.load(filename)
    else:
        net.random_init(RAND_IN, RAND_OUT, RAND_SIZE)

    net.print_info()
    net.check_network()

    results = net.step([True, False])
    print(results)

    net.save(filename)


if __name__ == '__main__':
    main()
