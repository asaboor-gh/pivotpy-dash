#Place Holder Variables.
JoinPathAt=None;E_Limit=None;E_Fermi=None;NKPTS=None;NBANDS=None;nField_Projection=None;
ProIndices=None;ProLabels=None;
import variables
import numpy as np
import shutil
import importlib as imp; #to reload module inside function
def datize(path='.',JoinPathAt=JoinPathAt,E_Limit=E_Limit,E_Fermi=E_Fermi,
           NKPTS=NKPTS,NBANDS=NBANDS,nField_Projection=nField_Projection,
           ProIndices=ProIndices,ProLabels=ProLabels):
    yh=max(E_Limit);yl=min(E_Limit); 
    data=np.loadtxt(path+'/Projection.txt')
    KE=np.loadtxt(path+'/Bands.txt')
    K=KE[:,3]; E=KE[:,4:]-E_Fermi; #Seperate KPOINTS and Eigenvalues in memory
    #Lets check if axis break exists
    try:
        JoinPathAt
    except NameError:
        JoinPathAt = []
    if(JoinPathAt):
        for pt in JoinPathAt:
            K[pt:]=K[pt:]-K[pt]+K[pt-1]
    #============Calculation of ION(s)-Contribution=======  
    #Get (R,G.B) values from projection and Normlalize in plot range
    maxEnergy=np.min(E,axis=0); minEnergy=np.max(E,axis=0); #Gets bands in visible energy limits.
    max_E=np.max(np.where(maxEnergy <=yh)); min_E=np.min(np.where(minEnergy >=yl))
    
    r_data=np.reshape(data,(-1,NKPTS,NBANDS,nField_Projection))
    s_data=np.take(r_data[:,:,min_E:max_E+1,:],ProIndices[0],axis=0).sum(axis=0)
    red=np.take(s_data,ProIndices[1],axis=2).sum(axis=2)
    green=np.take(s_data,ProIndices[2],axis=2).sum(axis=2)
    blue=np.take(s_data,ProIndices[3],axis=2).sum(axis=2)
    max_con=max(max(map(max,red[:,:])),max(map(max,green[:,:])),max(map(max,blue[:,:])))
    if(max_con!=0): 
        red=red[:,:]/max_con
        green=green[:,:]/max_con
        blue=blue[:,:]/max_con #Values are ready in E_Limit
    E=E[:,min_E:max_E+1]; #Updated energy in E_limit 
    #===============Make Collections======================
    text_plotly=[[str(ProLabels[1:])+'<br>RGB'+str((int(100*red[i,j]),int(100*green[i,j]),int(100*blue[i,j]))) for i in range(NKPTS)] for j in range (np.shape(E)[1])];
    rgb_plotly=[['rgb'+str((int(255*red[i,j]),int(255*green[i,j]),int(255*blue[i,j])))for i in range(NKPTS)] for j in range (np.shape(E)[1])];
    lw_plotly=[[np.round(1+20*(red[i,j]+green[i,j]+blue[i,j])/3,4) for i in range(NKPTS)] for j in range (np.shape(E)[1])]; # 1 as residual width
    return K,E,text_plotly,rgb_plotly,lw_plotly

#mouse event handler
def click_data(fig):
    def handle_click(trace, points, state):
        if(points.ys!=[]):
            print(np.round(float(points.ys[0])+E_Fermi,4))
    for i in range(len(fig.data)):
        trace=fig.data[i]
        trace.on_click(handle_click)


#Copy variables
def copy_here(path):
    shutil.copy(path+'/SysInfo.py','./variables.py') 
    #very start to load variables before using other one
    vbs=imp.reload(variables) #reload file after copied
    return vbs
#update ions and energy limit with new folder
def get_limits(path):
    vbs=copy_here(path)
    minE=-5#np.floor(vbs.E_core-vbs.E_Fermi)
    maxE=5#np.ceil(vbs.E_top-vbs.E_Fermi)
    marks={}; 
    for i in range(len(vbs.ElemName)):
        if(vbs.ElemIndex[i+1]-vbs.ElemIndex[i]>2):
            interval=int((vbs.ElemIndex[i+1]-vbs.ElemIndex[i])/2)
        else:
            interval=1
        for j in range(vbs.ElemIndex[i]+1,vbs.ElemIndex[i+1]+1,interval):
            marks.update( {j : vbs.ElemName[i]+':'+str(j)})
    maxION=vbs.ElemIndex[-1]
    return marks,maxION,minE,maxE