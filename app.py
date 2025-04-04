import dash
from dash import dcc, html, dash_table
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

# 데이터 로드
df = pd.read_csv('data/sales_data.csv')

# Dash 레이아웃
app.layout = html.Div([
    html.H1('회사 매출 데이터 포털'),
    html.H2('데이터 필터링'),
    dcc.Dropdown(
        id='product-dropdown',
        options=[{'label': '전체', 'value': 'All'}] + 
                [{'label': prod, 'value': prod} for prod in df['Product'].unique()],
        value=None,
        placeholder="제품 선택",
        style={'width': '50%'}
    ),
    html.H2('매출 데이터 테이블'),
    html.Div(id='table-container', style={'marginBottom': '20px'}),
    html.H2('매출 데이터 그래프'),
    dcc.Graph(id='sales-graph')
])

# 콜백 함수
@app.callback(
    [Output('table-container', 'children'),
     Output('sales-graph', 'figure')],
    [Input('product-dropdown', 'value')]
)
def update_output(selected_product):
    if selected_product == 'All' or selected_product is None:
        filtered_df = df
    else:
        filtered_df = df[df['Product'] == selected_product]
        if filtered_df.empty:
            return html.Div("선택한 제품에 대한 데이터가 없습니다."), px.bar()
    # dash_table로 테이블 렌더링
    table = dash_table.DataTable(
        data=filtered_df.to_dict('records'),
        columns=[{'name': col, 'id': col} for col in filtered_df.columns],
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left', 'padding': '8px'},
        style_header={'backgroundColor': '#4CAF50', 'color': 'white', 'fontWeight': 'bold'},
        style_data_conditional=[
            {'if': {'row_index': 'odd'}, 'backgroundColor': '#f2f2f2'}
        ]
    )
    fig = px.bar(filtered_df, x='Date', y='Sales', title='매출 데이터')
    return table, fig

if __name__ == '__main__':
    app.run(debug=False)