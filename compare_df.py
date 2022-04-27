# pip install pandas finplot==1.8.0

import pandas as pd
import finplot as fplt

timeFrame = "D1"
classCode = "TQBR"
classSecurities = ['IRAO', 'RTKM', 'TRMK']
classSecurities = ['TRMK']

csv_folder_quik = "csv_test_quik"
csv_folder_meta = "csv_test_mt5"


w = fplt.foreground = '#eef'
b = fplt.background = fplt.odd_plot_background = '#161a25'
fplt.candle_bull_color = fplt.volume_bull_color = '#26a69a'
fplt.candle_bull_body_color = '#1e6260'
fplt.volume_bull_body_color = '#1c5e5e'
fplt.candle_bear_color = fplt.volume_bear_color = '#ef5350'
fplt.candle_bear_body_color = '#86373b'
fplt.volume_bear_body_color = '#813539'
fplt.cross_hair_color = w + 'a'
# create axes
ax, ax2 = fplt.create_plot("ticker", rows=2)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    for secCode in classSecurities:
        file_quik = f"{csv_folder_quik}\\{classCode}.{secCode}_{timeFrame}.csv"
        file_meta = f"{csv_folder_meta}\\{classCode}.{secCode}_{timeFrame}.csv"
        try:
            df_quik = pd.read_csv(file_quik, sep=",", index_col="datetime")
            df_meta = pd.read_csv(file_meta, sep=",", index_col="datetime")
            print("df_quik:", df_quik, "df_meta:", df_meta, "\n---------------------------------------------------------")

            df_quik_1 = df_quik.drop(columns=["volume"])
            df_meta_1 = df_meta.drop(columns=["volume"])
            print("df_quik_1:", df_quik_1, "df_meta_1:", df_meta_1, "\n---------------------------------------------------------")

            df_diff = pd.concat([df_quik_1, df_meta_1]).drop_duplicates(keep=False) # оставляет различия из df_meta_1
            print(df_diff)

            df_diff = pd.concat([df_meta_1, df_quik_1]).drop_duplicates(keep=False)  # оставляет различия из df_quik_1
            print(df_diff)

        except:
            print("\n Error with ticker: ", secCode)

    data = df_quik

    data = data.reset_index()
    data.rename(columns={'datetime': 'Date', 'open': 'Open', 'high': 'High',
                         'low': 'Low', 'close': 'Close', 'volume': 'Volume'},
                inplace=True)  # Чтобы получить дату/время переименовываем колонки
    data.index = pd.to_datetime(data['Date'])
    print("ok2", data)

    # plot candles
    fplt.candlestick_ochl(data[['Open', 'Close', 'High', 'Low']], ax=ax)
    # plot volume
    fplt.volume_ocv(data[['Open', 'Close', 'Volume']], ax=ax2)  # ax=ax.overlay()
    fplt.show()

    print("\nDone.")