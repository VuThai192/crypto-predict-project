import plotly.graph_objects as go
from plotly.subplots import make_subplots

class ForecastVisualizer:
    def create_plot(self, history, forecast):
        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.1,
            row_heights=[0.7, 0.3]
        )
        
        # Price plot
        fig.add_trace(
            go.Scatter(
                x=history.index,
                y=history['close'],
                name='Historical Price',
                line=dict(color='#636EFA')
            ), row=1, col=1)
            
        fig.add_trace(
            go.Scatter(
                x=forecast['timestamps'],
                y=forecast['values'],
                name='Forecast',
                line=dict(color='#FFA15A', dash='dot')
            ), row=1, col=1)
            
        # Volume plot
        fig.add_trace(
            go.Bar(
                x=history.index,
                y=history['volume'],
                name='Volume',
                marker_color='#2ED9FF'
            ), row=2, col=1)
            
        fig.update_layout(
            template='plotly_dark',
            hovermode='x unified',
            title='24-Hour Crypto Price Forecast'
        )
        return fig