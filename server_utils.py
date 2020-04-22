import base64


def base64_str_to_bytearray(data) -> bytearray:
    decoded_data = base64.b64decode(data)
    data_as_str_list = str(decoded_data).split("\'")[1].split(",")
    data_as_int_list = [int(x) for x in data_as_str_list]
    return bytearray(data_as_int_list)