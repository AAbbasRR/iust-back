import random


def create_otp_code(length=5):  # create a random digit number
    return str(random.randint((10 ** (length - 1)), (10**length - 1)))


def generate_number(value, width=6):
    return f"{value:0{width}}"
