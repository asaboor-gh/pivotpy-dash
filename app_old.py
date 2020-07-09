import dash
from dash.dependencies import Input,Output,State
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import os
import shutil
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
def my_plot(index,red,green,blue,ions,E_Limit):
    ProLabels =['','s','p','d'];
    ProIndices =[list(range(ions[0]-1,ions[1],1)),red,green,blue];
    #====================Loading Files===================================
    #tick_plotly=[K[tickIndices[i]] for i in range(len(tickIndices))]; tlab_plotly=ticklabels;
    vbs=pf.copy_here(files[0][index]) #getting variables
    #global E_Fermi,NKPTS,NBANDS,nField_Projection,ElemIndex,ElemName,SYSTEM,E,K; #E must be global for monochrome/colorize
    SYSTEM=vbs.SYSTEM;
    E_Fermi,NKPTS,NBANDS,nField_Projection,ElemIndex,ElemName=vbs.E_Fermi,vbs.NKPTS,vbs.NBANDS,vbs.nField_Projection,vbs.ElemIndex,vbs.ElemName
    #getting sel_ion values
    options=[(ElemName[i],i+1) for i in range(len(ElemName))];options.append(('All',0))
    #sel_ion.options=options;sel_ion.value=0
    #============
    #global tab_data;
    tab_data=[]; #out.clear_output() #reset data output each time
    tab_data.append(['V',np.round(vbs.volume ,6),'&#8491<sup>3</sup>'])
    tab_data.append(['a',np.round(np.sqrt((np.array(vbs.basis[0])*np.array(vbs.basis[0])).sum()),8),'&#8491'])
    tab_data.append(['b',np.round(np.sqrt((np.array(vbs.basis[1])*np.array(vbs.basis[1])).sum()),8),'&#8491'])
    tab_data.append(['c',np.round(np.sqrt((np.array(vbs.basis[2])*np.array(vbs.basis[2])).sum()),8),'&#8491'])
    K,E,text_plotly,rgb_plotly,lw_plotly=pf.datize(path=files[0][index],JoinPathAt=given_data.JoinPathAt,E_Limit=E_Limit,E_Fermi=E_Fermi,
           NKPTS=NKPTS,NBANDS=NBANDS,nField_Projection=nField_Projection,
           ProIndices=ProIndices,ProLabels=ProLabels)
    #=================Plotting============================
    fig = go.Figure()
    for i in range(np.shape(E)[1]):
        fig.add_trace(go.Scatter(x=K,y=E[:,i],mode='markers+lines',hovertext=text_plotly[:][i],
                marker=dict(size=lw_plotly[:][i], color=rgb_plotly[:][i]) ,
                line=dict(color='rgba(100,100,20,0.1)',width=1.5),name='B<sub>{}</sub>'.format(str(i+1)) ))
    
    fig.update_layout(title=SYSTEM,autosize=True, width=400,height=320,
               margin=go.layout.Margin(l=60,r=50,b=40,t=75,pad=0),paper_bgcolor="whitesmoke",
                yaxis=go.layout.YAxis(title_text='E-E<sub>F</sub>',range=[np.min(E_Limit),np.max(E_Limit)]), 
              xaxis=go.layout.XAxis(ticktext=ticklabels, tickvals=[K[item] for item in tickIndices],
              tickmode="array",range=[K[0],K[-1]]),font=dict(family="stix, serif",size=14))
    fig.update_xaxes(showgrid=True, zeroline=False,showline=False, linewidth=0.1, linecolor='gray', mirror=True)
    fig.update_yaxes(showgrid=False, zeroline=True,showline=False, linewidth=0.1, linecolor='gray', mirror=True)
    #if there is break in KPath. Plot those lines
    for pt in given_data.JoinPathAt:
        x_k=[K[pt],K[pt]];y_k=[np.min(E_Limit),np.max(E_Limit)]
        fig.add_trace(go.Scatter(x=x_k,y=y_k,mode='lines',line=dict(color='whitesmoke',width=2),showlegend=False ))
    #fig.write_html("Interactive.html")
    #print("Time %s seconds ---" % (time.time() - start_time));start_time = time.time()
    #Handling mouse events
    #click_data()  #Only Required in Mian function
    #reset_E(None) #Only Required in Mian function
    return fig

app = dash.Dash()
sections=[]
sections.append(html.Div(className='AppHeader',id="drop1",children=[html.Div(className='CenHeader',children=html.P('Directory')),
    dcc.Dropdown( id="drop1-1",options=[{'label':files[0][i].split('III-V/')[1],'value' :i} for i in range(len(files[0]))],
    value=0,clearable=False),
    html.Div(className='CenHeader',id="drop1-2",children=[html.P('1/'+str(len(files[0])))])

]))
sections.append(html.Div(id='progressbar',children=html.Div(
style={"background":"#1f2c56","position":"fixed","width":str(1/len(files[0])*100)+"vw","height":"4px","left":"0px","right":"0px","top":"0px","z-index":"99999"})))
sections.append(html.Div(id="dd-output-container"))
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
#in start of app. ions are fully calculated.
N_sl=dcc.RangeSlider(id='ion_sl',min=1,max=variables.NION,value=[1,variables.NION],updatemode='mouseup',tooltip={"visible_always":False},vertical=True,verticalHeight=320)
E_range=dcc.RangeSlider(id='en_sl',min=-5,max=5,value=[-5,5],updatemode='mouseup',tooltip={"visible_always":False},vertical=True,verticalHeight=320)
sections.append(html.Div( style={"width":"280px","padding":"0.5px"}, children=[red_sl,grn_sl,blu_sl]))
#sections.append(html.Div(children=[N_sl,E_range]))
#here you can define your logic on how many times you want to loop

graph_=dcc.Graph(id='example-graph')

sections.append(html.Div(style={"display":"flex","padding":"2px"},children=[N_sl,E_range,graph_]))
global prev_t,next_t;
prev_t=html.Button(id='prev-btn',n_clicks=0, className="prev",style={"position": "fixed", "left": "0px", "top": "0px"},children=u'\u2039') #u'\u2b9c'+
next_t=html.Button(id='next-btn',n_clicks=0,className="next",style={"position": "fixed", "right": "0px", "top": "0px"},children=u'\u203a') #u'\u2b9e'+

sections.append(prev_t)
sections.append(next_t)
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
sections.append(html.Div(id='data_table')
    
)
app.layout = html.Div(style={"position": "absolute", "right": "50px","left":"50px","top":"50px","background":"#a5d6c2ee"},children=sections)

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
    return count_dir,maxION,ion_range,marks,minE,maxE,[lower,upper],mark_en


@app.callback(
    [Output('example-graph', 'figure'),Output('drop1-2', 'children'),Output('progressbar', 'children'),Output('data_table','children')],
    [Input('drop1-1', 'value'),Input('rs', 'value'),Input('gs', 'value'),Input('bs', 'value'),
    Input('ion_sl','value'),Input('en_sl','value')])
def update_fig(value,r_pro,g_pro,b_pro,ions,elim):
    return my_plot(index=value,red=r_pro,green=g_pro,blue=b_pro,ions=ions,E_Limit=elim),\
            html.P(str(value+1)+'/'+str(len(files[0]))),\
            html.Div(style={"background":"#1f2c56","position":"fixed","width":str((value+1)/len(files[0])*100)+"vw","height":"4px","left":"0px","right":"0px","top":"0px","z-index":"99999"}),\
            receive_data(index=value)


if __name__ == '__main__':
    app.run_server(debug=False)

