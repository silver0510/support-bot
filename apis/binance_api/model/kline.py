class Kline:
    def __init__(self, kline_arr):
        self.open_time = kline_arr[0]
        self.open_price = float(kline_arr[1])
        self.high_price = float(kline_arr[2])
        self.low_price = float(kline_arr[3])
        self.close_price = float(kline_arr[4])
        self.volume = float(kline_arr[5])
        self.close_time = kline_arr[6]
        self.quote_asset_volume = kline_arr[7]
        self.number_of_trades = kline_arr[8]
        self.taker_buy_base_asset_volume = kline_arr[9]
        self.taker_buy_base_quote_volume = kline_arr[10]
