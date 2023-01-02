### elliott main py
import os
import time
import random

from dash import Dash, html, dcc, Output, Input
import plotly.graph_objs as go
import plotly.express as px
import dash_daq as daq

from data.simulator import simulator
from models.wave_detector import monowave
from models.identifier import identifier
from assets.webcomponents import webcomp
web=webcomp()
data_path=os.path.join(os.getcwd(),'data/btcusd.csv')

class plotWeb:
    def __init__(self,data_path):
        self.data_path=data_path
        self.sim=simulator(self.data_path)
        self.mon=monowave()
        self.sim()
        self.idf=identifier()

        #dash by plotly

        self.app=Dash(__name__)
        self.application = self.app.server

        self.app.layout=html.Div(
            children=[
                dcc.Markdown(web.title),
                html.Div([
                    html.B(web.version, style={'textAlign': 'right'}),
                    html.Br(),
                    html.A(href='https://github.com/minimikim',
                            target="_blank",
                            children=[
                                html.Img(
                                    alt='githublink_1',
                                    src='assets/mk.png',
                                    style=web.git_image_style
                                )
                            ],
                            ),
                    #html.Br(),
                    html.A(href='https://github.com/nowinseason',
                            target="_blank",
                            children=[
                                html.Img(
                                    alt='githublink_2',
                                    src='assets/ch.png',
                                    style=web.git_image_style
                                )
                            ],
                            ),
                    ],
                    style={'textAlign':'right'}),
                dcc.Graph(
                    id='graph'
                    ),
                html.Div([
                    html.Button('Refresh', id='my-button'),
                    html.P(id='refreshed',style={'display':'none'})
                ],
                    style={'textAlign':'center'},
                           ),
                html.Br(),
                html.Div([
                    'Input : ',
                    dcc.Input(
                        id='input',
                        value='Random Starts',
                        type='number',
                        debounce=True,
                        placeholder="Range 1 to 100000")],
                    style={"textAlign":'center'}),
                html.Div(
                    id='start_idx',
                    style={'textAlign':'center'}),

                daq.BooleanSwitch(
                    id='my-boolean-switch',
                    on=False,
                    disabled=False),

                dcc.Interval(
                    id='interval_component',
                    interval=1000,
                    n_intervals=0),
                html.Br(),
                dcc.Markdown(web.intro),
                html.Iframe(
                    src="assets/tutorial.html",
                    style={"height": "1067px",
                           "width": "100%",
                           'border':"0",
                          # "marginLeft":300,
                           #"marginRight":300,
                           'textAlign':'center'}),
        ],style={"marginLeft":100,
                 "marginRight":100,
                 "marginTop":50,
                 })
        self.app.callback(
            Output('refreshed','children'),
            [Input('my-button', 'n_clicks')]
        )(self.refresh)

        self.app.callback(
            Output('start_idx','children'),
            Input('input','value')
        )(self.update_init)

        self.app.callback(
            Output('graph','figure'),
            [Input('my-boolean-switch', 'on'),
            Input('interval_component','n_intervals')]
        )(self.update_graph)

    def refresh(self,n_clicks):
        if n_clicks>0:
            self.mon=monowave()
            self.sim=simulator(self.data_path)
            self.sim()
            self.idf=identifier()
        return f'Refreshed'


    def update_init(self,value):
        print('idx start from {}'.format(value))
        self.sim(value)
        return f'Output : {value}'

    def update_graph(self,on,n):
        if on:
            self.wave_detect()
            fig=self.figure()

            return fig
        else:
            fig=self.figure()
            return fig

    def wave_detect(self):
        self.price=self.sim.gen()
        self.mon.add(self.price)
        self.mon.analyze()
        self.idf.monowave=self.mon.group_monowave
        self.idf()

    def figure(self):
        fig=go.Figure([go.Scatter(x=self.sim.gen_time,
                                  y=self.mon.price,
                                  name='Price')])
        fig.add_trace(go.Scatter(x=self.sim.gen_time,
                                 y=self.mon.newline,
                                 opacity=0.7,
                                 name='Monowave'))
        for i in range(len(self.mon.group_monowave)):
            m_idx=self.mon.group_monowave[i][-1]

            fig.add_annotation(
                x=self.sim.gen_time[m_idx],
                y=self.mon.price[m_idx],
                text=''.join(['M',str(i+1)]),
                yshift=10,
                showarrow=False,
                arrowcolor='#CBDCCB',
                arrowsize=0.3,
                hovertext=self.ident_label(m_idx,self.idf.logic),)

        fig.layout.template='plotly_white'

        return fig

    @staticmethod
    def ident_label(idx,dic):
        if dic.get(idx):
            return str(dic[idx])
        else:
            return None

def main():
    plot=plotWeb(data_path)
    app=plot.app
    app.run_server(debug=True)
    #plot.application.run_server(debug=True)

if __name__=="__main__":
    print('start!')
    main()



# def main():
#     plot=plotWeb(data_path)
#     plot.app.run_server(debug=True)
#     #simulator setting
#     sim=simulator(data_path)
#     sim(5570)
#     #detector setting
#     mon=monowave()
#     idf=identifier()
#     while True:
#         time.sleep(0.3)
#         #1. simulator bring realtime price data
#         price=sim.gen()
#         mon.add(price)
#         idf.add(price)
#         #2. detector save the price data and fit monowave
#         mon.analyze()
#         idf.monowave=mon.group_monowave
#         idf()
#         #3. plot the elliott wave as graph and update log
#         #plotting output
#
