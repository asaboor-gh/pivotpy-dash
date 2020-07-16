import dash
from dash.dependencies import Input,Output,State
import dash_core_components as dcc
import dash_html_components as html
import pivotpy as pp
import numpy as np
import os
import shutil
import json
import importlib as imp; #to reload module inside function
import plotly.graph_objs as go
import pivotpy.g_utils as sf
import PlotlyFile as pf
import variables
import InputFile
import pandas as pd
count_dir = 0 #place holder 
given_data=imp.reload(InputFile) #reload
files=sf.select_dirs(path=given_data.ParentFolder, include=given_data.IncludeFolders)
tickIndices =given_data.TickIndices;
ticklabels =given_data.TickLabels;


#Plot Function.
def my_plot(evr,red,green,blue,ions,E_Limit):
    ProLabels =['','s','p','d'];
    ProIndices =[range(ions[0]-1,ions[1],1),red,green,blue];
    fig = pp.plotly_rgb_lines(path_evr = evr,ions=ProIndices[0],orbs=ProIndices[1:],orblabels=ProLabels[1:],elim=E_Limit,joinPathAt=given_data.JoinPathAt)
    #============
    #global tab_data;
    # tab_data=[]; #out.clear_output() #reset data output each time
    # tab_data.append(['V',np.round(vbs.volume ,6),'&#8491<sup>3</sup>'])
    # tab_data.append(['a',np.round(np.sqrt((np.array(vbs.basis[0])*np.array(vbs.basis[0])).sum()),8),'&#8491'])
    # tab_data.append(['b',np.round(np.sqrt((np.array(vbs.basis[1])*np.array(vbs.basis[1])).sum()),8),'&#8491'])
    # tab_data.append(['c',np.round(np.sqrt((np.array(vbs.basis[2])*np.array(vbs.basis[2])).sum()),8),'&#8491'])
    #fig.write_html("Interactive.html")
    #print("Time %s seconds ---" % (time.time() - start_time));start_time = time.time()
    #Handling mouse events
    #pf.click_data(fig=fig)  #Only Required in Mian function
    #reset_E(None) #Only Required in Mian function
    return fig
def receive_data(index):
    df=pd.read_csv(files[0][index]+'/Result.txt',sep='\t',header=None).dropna(axis=1).dropna(axis=0)
    return html.Div(children=[
        html.Table([
            html.Tr([html.Th('V('+u'\u212B\u00B3'+')') if 'V' in word else html.Th(word+'('+u'\u212B'+')') for word in df[0][:4]]),
            html.Tr([html.Td(val) for val in df[1][:4]])
            ]),
        html.P(),
        html.Table([
            html.Tr([html.Th([html.B('E'),html.Sub('gap'),html.B('(eV)')]) if 'gap' in word else html.Th([html.B('Δ'),html.Sub('SO'),html.B('(eV)')]) if '\Delta' in word else html.Th([html.B('E'),html.Sub('core'),html.B('(eV)')]) if 'core' in word else html.Th(word+'(eV)') for word in df[0][4:]]),
            html.Tr([html.Td(val) for val in df[1][4:]]) ]) ])

app = dash.Dash()
sections=[]
sections.append(html.Div(className='AppHeader',id="drop1",children=[html.Div(className='CenHeader',children=html.P('Directory')),
    dcc.Dropdown(className='CenHeader', id="drop1-1",options=[{'label':files[0][i].split('III-V/')[1],'value' :i} for i in range(len(files[0]))],
    value=0,clearable=False),
    html.Div(className='CenHeader',id="drop1-2",children=[html.P('1/'+str(len(files[0])))])

]))
sections.append(html.Div(className="logo",style={"box-shadow":"none","border":"none","background":"none"},children=[html.H1('Pivotpy-Dash')]))
sections.append(html.Div(id='progressbar',children=html.Div(
style={"background":"#1f2c56","position":"fixed","width":str(1/len(files[0])*100)+"vw","height":"4px","left":"0px","right":"0px","top":"0px","z-index":"99999"})))
sections.append(html.Div(id="dd-output-container"))
sections.append(html.Div(className="result_table",id='data_table'))
#B0_py      B0_pz      B0_px      B0_dxy      B0_dyz      B0_dz2      B0_dxz      B0_x2-y2
pro_list=['s','py','pz','px','dxy','dyz','dz2','dxz','dx2-y2']
pro_ind=[0,1,2,3,4,5,6,7,8]

red_sl=dcc.Dropdown(id='rs',persistence=True,placeholder='Select Red',
    options=[{'label': item, 'value': ind} for item,ind in zip(pro_list,pro_ind)],
    value=0,clearable=False,multi=True) 
grn_sl=dcc.Dropdown(id='gs',persistence=True,placeholder='Select Green',
    options=[{'label': item, 'value': ind} for item,ind in zip(pro_list,pro_ind)],
    value=[1,2,3],clearable=False,multi=True) 
blu_sl=dcc.Dropdown(id='bs',persistence=True,placeholder='Select Blue',
    options=[{'label': item, 'value': ind} for item,ind in zip(pro_list,pro_ind)],
    value=[4,5,6,7,8],clearable=False,multi=True) 
ions_sl=dcc.Dropdown(id='ions',persistence=True,placeholder='Select IONS',
    options=[{'label': item, 'value': ind} for item,ind in zip(pro_list,pro_ind)],
    value=[4,5,6,7,8],clearable=False,multi=True) 
#in start of app. ions are fully calculated.
N_sl=dcc.RangeSlider(id='ion_sl',min=1,max=variables.NION,value=[1,variables.NION],updatemode='mouseup',vertical=True)
E_range=dcc.RangeSlider(id='en_sl',min=-5,max=5,value=[-5,5],updatemode='mouseup',vertical=True)
sections.append(html.Div(className = "orbitals", children=[html.H6('Select Orbitals'),red_sl,grn_sl,blu_sl,html.H6('Select Sites'),ions_sl]))
#sections.append(html.Div(children=[N_sl,E_range]))
#here you can define your logic on how many times you want to loop
store=dcc.Store(id="store")
_out_put = html.Div(id="output")
graph_=html.Div(className="graphDiv", children = dcc.Loading(className="loading", children=dcc.Graph(className="graph",id='example-graph',config = {'responsive': True}),type='default'))

sections.append(html.Div(className="gr_sl",style={"display":"flex","padding":"20px"},children=[N_sl,E_range,graph_,_out_put,store]))
global prev_t,next_t;
prev_t=html.Button(id='prev-btn',n_clicks=0, className="prev",style={"position": "fixed", "left": "0px", "top": "0px"},children=u'\u2039') #u'\u2b9c'+
next_t=html.Button(id='next-btn',n_clicks=0,className="next",style={"position": "fixed", "right": "0px", "top": "0px"},children=u'\u203a') #u'\u2b9e'+

sections.append(prev_t)
sections.append(next_t)


app.layout = html.Div(className="wrap",style={"position": "absolute", "right": "50px","left":"50px","top":"60px","background":"whitesmoke"},children=sections)

@app.callback(Output('dd-output-container', 'children'),
    [Input('rs', 'value'),Input('gs', 'value'),Input('bs', 'value')])
def update_output(value,value2,value3):
    return 'Red: "{}" and Green:  "{}" and Blue: "{}" '.format(value,value2,value3)
#order of callbacks matters
@app.callback([Output('drop1-1', 'value'),
    Output('ion_sl','max'),Output('ion_sl','value'),Output('ion_sl','marks'),
    Output('en_sl','min'),Output('en_sl','max'),Output('en_sl','value'),Output('en_sl','marks'),],
    [Input('next-btn', 'n_clicks'),Input('prev-btn', 'n_clicks')],
    [State('drop1-1','value'),State('en_sl','value'),State('ion_sl','value')])
def update_dir(cl_1,cl_2,st_1,elim,ion):
    ctx = dash.callback_context
    if not ctx.triggered:
        button_id = 'No clicks yet'
        count_dir=st_1
    else:
        button_id = ctx.triggered[0]['prop_id']
        if(button_id in "next-btn.n_clicks"):
            count_dir=st_1+1
        if(button_id in "prev-btn.n_clicks"):
            count_dir=st_1-1
    if(count_dir>len(files[0])-1):
        count_dir=len(files[0])-1
    if(count_dir<0):
        count_dir=0
    #use this count_dir to update dropdown.
    vbs=pf.copy_here(files[0][count_dir])
    marks,maxION,minE,maxE=pf.get_limits(files[0][count_dir]) 
    if(np.min(elim)<minE):  #This part is for smooth experience.
        lower=minE
    else:
        lower=np.min(elim)
    if(np.max(elim)>maxE):
        upper=maxE
    else:
        upper=np.max(elim)
    if(ion[1]<=maxION):  #return same range of ions. for consistency. Only change with different NION
        ion_range=ion        
    else:
        ion_range=[1,maxION]  
    mark_en={} #Just to make clear without click.
    for point in range(int(minE),int(maxE)+1,2):
        mark_en.update({point: str(point)})
    print("E_min: {}".format(minE))
    return count_dir,maxION,ion_range,marks,minE,maxE,[lower,upper],mark_en


@app.callback(Output('store', 'data'),[Input('drop1-1', 'value')])
def export_to_store(index):
    import pivotpy as pp 
    vr = pp.export_vasprun(path=files[0][index]+'/vasprun.xml',joinPathAt=given_data.JoinPathAt)
    print(vr.keys())
    vr.pop('xml',None)
    s=json.dumps(vr, cls=pp.EncodeFromNumpy)
    return s

@app.callback(
    [Output('example-graph', 'figure'),Output('drop1-2', 'children'),Output('progressbar', 'children'),Output('data_table','children')],
    [Input('drop1-1', 'value'),Input('rs', 'value'),Input('gs', 'value'),Input('bs', 'value'),
    Input('ion_sl','value'),Input('en_sl','value'),Input('store','data')])
def update_fig(value,r_pro,g_pro,b_pro,ions,elim,data):
    import pivotpy as pp
    s2 = json.loads(data,cls= pp.DecodeToNumpy)
    evr = pp.make_dot_dict(s2)
    import plotly.graph_objs as go
    return my_plot(evr=evr,red=r_pro,green=g_pro,blue=b_pro,ions=ions,E_Limit=elim),\
            html.P(str(value+1)+'/'+str(len(files[0]))),\
            html.Div(style={"background":"#1f2c56","position":"fixed","width":str((value+1)/len(files[0])*100)+"vw","height":"4px","left":"0px","right":"0px","top":"0px","z-index":"99999"}),\
            receive_data(index=value)
@app.callback(
    Output('output', 'children'),
    [Input('example-graph', 'clickData'),Input('store','data')])
def display_click_data(clickData,data):
    json.loads(data)
    #print("Stored : {}".format(data))
    if(clickData):
        print("X : {}".format(clickData['points'][0]['x']))
        print("Y : {}".format(clickData['points'][0]['y']))
        return html.P("X : {}, Y : {}".format(clickData['points'][0]['x'],clickData['points'][0]['y']+variables.E_Fermi))

if __name__ == '__main__':
    app.run_server(debug=False)

