"""
fiat(RUB) -p2p-> crypto(ByBit) -spot-> crypto(ByBit) -p2p-> fiat(RUB)
"""
from bybit_operations import *
from bybit_constants import *
from Block import *


def v1_y(amount, units):
    output = []
    startBlock = Block_start((amount, units))

    def phase1():
        for token in ALL_CRYPTO:
            newBlock = p2p_buy(startBlock, token)
            print(newBlock)
            assert type(newBlock) == Block_buy
            phase2(newBlock)
            phase3(newBlock)

    def phase2(thisBlock):
        print(thisBlock)
        blockUnits = thisBlock.units
        for token in ALL_CRYPTO:
            if blockUnits == token:
                continue
            newBlock = spot(block=thisBlock, token=token)
            assert type(newBlock) == Block_change
            phase3(newBlock)

    def phase3(thisBlock):
        global output_data
        global file
        assert type(thisBlock) in [Block_buy, Block_change]
        newBlock = p2p_sell(thisBlock, startBlock.units)
        # print(newBlock)
        if newBlock.crush:
            return

        print(newBlock)

        if newBlock.amount / startBlock.amount > 1:
            # file.write('BYBIT\n\n' + str(newBlock))
            output_data += 'BYBIT\n\n' + str(newBlock)
            file = open('../../chains.txt', 'wt')
            file.write(output_data)
            file.close()

    phase1()


output_data = ''

if __name__ == "__main__":
    import time

    while True:
        output_data = ''
        v1_y(100000, RUB)
        file = open('../../chains.txt', 'wt')
        file.write(output_data)
        file.close()
        time.sleep(120)