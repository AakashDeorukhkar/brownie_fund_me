from brownie import FundMe, MockV3Aggregator, network, config
from scripts.helpful_scripts import (
    get_account,
    deploy_mocks,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)
from web3 import Web3
from brownie.network import gas_price
from brownie.network.gas.strategies import LinearScalingStrategy

# Added to fix memepool issue...
gas_strategy = LinearScalingStrategy("60 gwei", "70 gwei", 1.1)
gas_price(gas_strategy)


# if we are on a persistant network like Goerli testnet, use the associated address
# Otherwise, deploy mocks
def deploy_fund_me():
    account = get_account()
    # Check for testnet and import addresses from brownie-config.yaml
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]  # "0xD4a33860578De61DBAbDc8BFdb98FD742fA7028e"
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account, "gas_price": gas_strategy},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )  # publish_source=True) To publish out code
    print(f"Contract deployed to {fund_me.address}")
    return fund_me


def main():
    deploy_fund_me()
