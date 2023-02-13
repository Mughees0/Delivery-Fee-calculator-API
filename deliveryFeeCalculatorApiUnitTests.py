##### THIS IS THE API TEST FILE #####

from deliveryFeeCalculatorApi import *

# cartValueSurchargeCalc() tests


def test_surcharge():
    assert cartValueSurchargeCalc(500) == 500

# deliveryDistanceFeeCalc() tests


def test_DeliveryDistance():
    assert deliveryDistanceFeeCalc(1000) == 200


def test_DeliveryDistance1():
    assert deliveryDistanceFeeCalc(1499) == 300


def test_DeliveryDistance2():
    assert deliveryDistanceFeeCalc(1500) == 300


def test_DeliveryDistance3():
    assert deliveryDistanceFeeCalc(1501) == 400

# itemsSurchargeCalc() tests


def test_itemSurchargeCost():
    assert itemsSurchargeCalc(4) == 0


def test_itemSurchargeCost1():
    assert itemsSurchargeCalc(5) == 50


def test_itemSurchargeCost2():
    assert itemsSurchargeCalc(9) == 250


def test_itemSurchargeCost3():
    assert itemsSurchargeCalc(10) == 300


def test_itemSurchargeCost4():
    assert itemsSurchargeCalc(13) == 570


# rushHourSurchargeCalc() tests
def test_fridayRushCost():
    assert rushHourSurchargeCalc("2023-01-27T15:00:00Z", 710) == 852


def test_fridayRushCost1():
    assert rushHourSurchargeCalc("2021-10-12T13:00:00Z", 710) == 710


def test_fridayRushCost2():
    assert rushHourSurchargeCalc("2023-01-31T16:00:00Z", 710) == 710


# deliveryFee() tests
def test_deliveryFee():
    assert deliveryFee(790, 710) == 710


def test_deliveryFee1():
    assert deliveryFee(10456, 710) == 0


def test_deliveryFee2():
    assert deliveryFee(790, 7104784) == 1500


def test_responseType():
    assert type(deliveryFee(790, 710)) is int
