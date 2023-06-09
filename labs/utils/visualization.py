import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def candle_stick(series, ticker, close="adj_close"):
    series["timestamp"] = pd.to_datetime(series.index, unit="s")
    fig = go.Figure(
        data=[
            go.Candlestick(
                x=series["timestamp"],
                open=series["open"],
                high=series["high"],
                low=series["low"],
                close=series[close],
            )
        ]
    )

    fig.update_layout(
        title=f"Candlestick Chart {ticker}",
        xaxis_title="Date",
        yaxis_title="Price",
        width=1000,
        height=800,
    )

    fig.show()


def multiple_line_chart(datasets, tickers, feature="adj_close"):
    fig = make_subplots(rows=len(datasets), cols=1)

    for i, data in enumerate(datasets):
        data["timestamps"] = pd.to_datetime(data.index, unit="s")
        fig.add_trace(
            go.Scatter(
                x=data.timestamps, y=data[feature], mode="lines", name=tickers[i]
            ),
        )

    fig.update_layout(height=600, width=800, title="Data timeseries nilai mata uang")
    fig.update_xaxes(title="Tanggal", row=len(datasets), col=1)

    for i, data in enumerate(datasets):
        fig.update_yaxes(title_text="Close Price", row=i + 1, col=1)

    fig.show()
