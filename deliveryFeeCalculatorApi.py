##### THIS IS THE MAIN API FILE OF THE PROJECT #####

# libraries
from flask import *
from datetime import *
from dateutil import parser
import re

# initializing the API app
app = Flask(__name__)


# sub functions start ---------------------------------------------------------

def cartValueSurchargeCalc(cart_value):
    if (cart_value < 1000):
        # surcharge is the difference between the cart value and 1000c
        surcharge = 1000 - cart_value
        return surcharge
    else:
        return 0


def deliveryDistanceFeeCalc(delivery_distance):
    if (delivery_distance > 1000):

        # 100c is added for every additional 500 meters

        # 500.1 will always give float value
        # int function will trim value e.g. 2.99 = 2
        # then adding 1 for the next 500 meters
        fee = (int(delivery_distance / 500.1) + 1) * 100
        return fee
    else:
        # 200c
        return 200


def itemsSurchargeCalc(number_of_items):
    if (number_of_items > 4):
        # number of items above 4 will have 50c per item surcharge
        extra_item_fee = (number_of_items - 4) * 50

        if (number_of_items > 12):
            # number of items above 12 will have additional 120c per item surcharge
            total_fee = ((number_of_items - 12) * 120) + extra_item_fee
            return total_fee
        else:
            return extra_item_fee
    else:
        return 0


def rushHourSurchargeCalc(timestamp, total_fee):

    # check weekday from timestamp
    weekday = (parser.parse(timestamp)).isoweekday()

    # check hour from timestamp
    hour = (timestamp[11] + timestamp[12])

    # Friday rush (3 - 7 PM UTC)
    if (weekday == 5 and hour >= "15" and hour <= "19"):

        # delivery fee will be multiplied by 1.2x
        return (total_fee * 1.2)
    else:
        return total_fee


# This function calculates the total delivery fee and will return the HTML response below

def deliveryFee(cart_value, total_fee):
    if (cart_value >= 10000):
        return 0
    else:
        if (total_fee > 1500):
            return 1500
        else:
            return total_fee


# sub functions end ---------------------------------------------------------


# POST API - calculating delivery fee
@app.route('/', methods=['POST'])
# main function
def ReturnJSON():

    # save the input json from api request body
    in_data = request.get_json()

    # check input data types
    if (type(in_data['cart_value']) == int and type(in_data['delivery_distance']) == int and type(in_data['number_of_items']) == int and type(in_data['time']) == str):

        # time should be in ISO Format e.g. "2021-10-12T13:00:00Z"
        if re.match(r"\d{4}-[0-1]\d-[0-3]\dT[0-2]\d:[0-5]\d:[0-5]\dZ", in_data["time"]):
            pass

        else:
            data = {'error code': 400,
                    'message': 'The timestamp is not in ISOformat'}
            return (data), 400

    else:
        data = {'error code': 400, 'message': 'Input data types are incorrect'}
        return (data), 400

    # small order surcharge calculation
    surcharge = cartValueSurchargeCalc(in_data["cart_value"])

    # delivery distance surcharge calculation
    delivery_distance_surcharge = deliveryDistanceFeeCalc(
        in_data["delivery_distance"])

    # number of items surcharge calculation
    item_surcharge = itemsSurchargeCalc(in_data["number_of_items"])

    # total fee for rush hour calculation
    total_fee = surcharge + delivery_distance_surcharge + item_surcharge

    friday_rushhour_surcharge = rushHourSurchargeCalc(
        in_data["time"], total_fee)

    # delivery fee calculation
    delivery_fee = deliveryFee(
        in_data["cart_value"], friday_rushhour_surcharge)

    # api response
    data = {"delivery_fee": delivery_fee}

    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
