# from pybricks.utility.datatype import hello_world
from pybricks.market_data.market_data import load_market_data, calculate_xma

print("Starting the applicaiton pybricks...")


def main(action):
    if (action == 'data_load'):
        print('Loading the market data')
        load_market_data()

    if (action == 'calc_xma'):
        calculate_xma()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='My Portfolio Utility')

    parser.add_argument('--action', metavar='path',
                        required=True, help='action to be performed')

    args = parser.parse_args()
    print('Passed in action is {0}'.format(args.action))

    main(args.action)
