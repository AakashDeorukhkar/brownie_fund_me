from brownie import network, config, accounts, MockV3Aggregator
from web3 import Web3

DECIMALS = 8
STARTING_PRICE = 200000000000
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]


def get_account():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def deploy_mocks():
    print(f"The active network is {network.show_active()}")
    print("Deploying Mocks...")
    if len(MockV3Aggregator) <= 0:
        MockV3Aggregator.deploy(
            DECIMALS,
            STARTING_PRICE,
            # Web3.toWei(STARTING_PRICE, "ether"),
            {
                "from": get_account()
            },  # toWei will add 18 decible places to the number i.e 2000 here
        )  # from constructor(uint8 _decimals, int256 _initialAnswer)
        # Acesses the most recently deployed MockV3Aggregator
        print("Mocks Deployed")
