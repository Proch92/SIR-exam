from network import Network


def main():
    net = Network(2, 2, graph_size=10)
    results = net.step([True, False])
    print(results)


if __name__ == '__main__':
    main()
