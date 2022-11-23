import json


def print_json(json_string):
    print(json.dumps(json_string, indent=2))


def get_pivot_low_high(data, period):
    highs = []
    lows = []
    for i in range(len(data)):
        if i < period or i > (len(data) - period - 1):
            highs.append(0)
            lows.append(0)
        else:
            check_range = data[(i - period):(i + period + 1)]
            if data[i] == max(check_range):
                highs.append(data[i])
            else:
                highs.append(0)

            if data[i] == min(check_range):
                lows.append(data[i])
            else:
                lows.append(0)

    return highs, lows
