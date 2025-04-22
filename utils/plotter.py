import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

class ForecastVisualizer:
    def create_plot(self, history_df, predictions, future_steps=48, interval_minutes=30):
        """Tạo biểu đồ kết hợp lịch sử và dự báo"""
        # Kiểm tra và chuyển đổi index thành datetime
        if not pd.api.types.is_datetime64_any_dtype(history_df.index):
            history_df.index = pd.to_datetime(history_df.index, unit='s')  # Giả sử timestamp là Unix time (seconds)
        
        # Tạo mốc thời gian cho dự báo
        last_timestamp = history_df.index[-1]
        time_points = pd.date_range(
            start=last_timestamp + pd.Timedelta(minutes=interval_minutes),
            periods=future_steps,
            freq=f'{interval_minutes}min'  # Đã sửa 'T' → 'min'
        )

        fig = make_subplots(rows=2, cols=1, shared_xaxes=True)

        # Vẽ dữ liệu lịch sử
        fig.add_trace(go.Candlestick(
            x=history_df.index,
            open=history_df['open'],
            high=history_df['high'],
            low=history_df['low'],
            close=history_df['close'],
            name='Giá thực tế'
        ), row=1, col=1)

        # Vẽ dự báo
        fig.add_trace(go.Scatter(
            x=time_points,
            y=predictions,
            mode='lines+markers',
            name='Dự báo 24h',
            line=dict(color='#FF6B6B')
        ), row=1, col=1)

        # Vẽ volume
        fig.add_trace(go.Bar(
            x=history_df.index,
            y=history_df['volume'],
            name='Khối lượng',
            marker_color='#2ED9FF'
        ), row=2, col=1)

        fig.update_layout(
            title='Dự báo giá Crypto 24 giờ',
            template='plotly_dark',
            hovermode='x unified',
            height=800
        )

        return fig