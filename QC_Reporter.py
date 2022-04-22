#!/usr/bin/env python
# coding: utf-8

# In[11]:


#import pandas for dataframes, import seaborn for graphs, import csv, import os for file handling
import matplotlib
matplotlib.use('PDF')
import matplotlib.pyplot as plt
import pandas as pd
import os
import webbrowser
import math
import seaborn as sns

global df
csv_name = '/datain/pipeline_outputs_SUB_02-04-2022.csv' #INPUT csv name here
df = pd.read_csv(csv_name) #import csv

list_outliers = {} #global list of outliers for later use

study_name = csv_name.split("_")[2]
tmp = csv_name.split(".")[0]
date_dash = tmp.split("_")[3]
date = date_dash.replace("-", "/") #INPUT date updated (mm/dd/yyyy)


#drop unneeded columns ---> FOR USE WITH PAUL'S OUTPUTS ONLY, COMMENT OUT FOR OTHER STUDIES
for col in df.columns:
    if (('MaximizedModularity' in col) 
        or ('MeanTotalStrength'in col)
        or ('NetworkCharacteristic' in col) or ('TotalStrength' in col)
        or ('dummyrest' in col) or ('session_id' in col)
        or ('dummy_rest' in col) or ('file_name' in col) or ('1back' in col)
        or ('acq_id' in col)):
        del df[col]

#filter id columns to include only integers
for id in df['subject_id'].dropna():
    if(len(id)>4):
        idnum=id[-4:]
        df['subject_id']=df['subject_id'].replace(id,idnum) 


# In[3]:


#create graphs
plt.switch_backend('Agg')
for i,col in enumerate(df.columns):
    try:
        plt.figure(i) #blank plot, to load graphs
        plt.ion()
        ax = sns.scatterplot(x='subject_id',y=col, data=df)
        std_line = df[col].std()
        ax = sns.lineplot(x='subject_id',y=std_line+df[col].mean(), data=df)
        ax = sns.lineplot(x='subject_id',y=-1*std_line+df[col].mean(), data=df)
        ax = sns.lineplot(x='subject_id',y=2*std_line+df[col].mean(), data=df)
        ax = sns.lineplot(x='subject_id',y=-2*std_line+df[col].mean(), data=df)
        ax.set_xticklabels(df['subject_id'],rotation=270)
        fig = ax.get_figure() 
        plt.ioff()
        fig.savefig(col+'.png',backend='Agg') #save each plot in local folder
        
        
    except TypeError:
        print('Graph not generated for: '+col) 


# In[4]:


#create descriptions for different variables using keywords, return corresponding string
def desc(name):
    if('snrd' in name):
        return 'Dietrich’s SNR using air background as reference:<span style="color: green"> &#8593</span>'
    elif('snr' in name or 'tsnr' in name):
        return 'Signal-to-Noise ratio:<span style="color: green"> &#8593</span>'
    elif('cnr' in name):
        return 'Contrast-to-noise ratio:<span style="color: green"> &#8593</span>'
    elif('fwhm' in name):
        return 'Full-width half maximum estimations:<span style="color: green"> &#8595</span>'
    elif('qi2' in name):
        return 'Goodness of fit of a noise model into the background noise: <span style="color: green">&#8595</span>'
    elif('cjv' in name):
        return 'Coefficient of joint variation:<span style="color: green"> &#8595</span>'
    elif(name.startswith('efc')):
        return """Entropy focus criterion:
        <span style="color: green"> &#8595 more uniform distribution, less noisy</span>"""
    elif('fber' in name):
        return 'Foreground-background energy ratio:<span style="color: green"> &#8593</span>'
    elif('qi1' in name):
        return 'Segmentation using mathematical morphology:<span style="color: green"> &#8595</span>'
    elif('inu' in name):
        return 'Intensity non-uniformity estimate measurements:<span style="color: green"> ~1</span>'
    elif('pve' in name):
        return 'Partial volume errors:<span style="color: green"> &#8595</span>'
    elif('wm2max' in name):
        return 'White-matter to maximum intensity ratio:<span style="color: green"> [0.6, 0.8]</span>'
    elif('icv' in name):
        return 'Intracranial volume fractions: <span style="color: green"> “should move within a normative range”</span>'
    elif('rpve' in name):
        return 'Residual partial volume errors:<span style="color: green"> &#8595</span>'
    elif('fd' in name):
        return 'Framewise displacement:<span style="color: green"> &#8595</span>'
    elif('dvars' in name):
        return 'Temporal derivative of timecourses RMS variance over voxels:<span style="color: green"> &#8595</span>'
    elif('gsr' in name):
        return 'Ghost-to-signal Ratio:<span style="color: green"> &#8595</span>'
    elif('gcor' in name):
        return 'Global correlation :<span style="color: green"> &#8595</span>'
    elif('spikes' in name):
        return 'High frequency and global intensity :<span style="color: green"> &#8595 (lessvolumes to remove if filtering)</span>'
    elif('aor' in name):
        return 'AFNI’s outlier ratio: mean fraction of outliers per fMRI volume'
    elif('aqi' in name):
        return 'AFNI’s quality index: mean quality index'
    elif('coregCrossCorr' in name):
        return 'Cross correlation:<span style="color: green"> &#8593</span>'
    elif('CoregJaccard' in name):
        return 'Jaccard index:<span style="color: green"> &#8593</span>'
    elif('CoregDice' in name):
        return 'Dice index:<span style="color: green"> &#8593</span>'
    elif('CoregCoverage' in name):
        return 'Coverage index:<span style="color: green"> &#8593</span>'
    elif('regCrossCorr' in name):
        return 'Cross correlation:<span style="color: green"> &#8593</span>'
    elif('regJaccard' in name):
        return 'Jaccard index:<span style="color: green"> &#8593</span>'
    elif('regDice' in name):
        return 'Dice index:<span style="color: green"> &#8593</span>'
    elif('regCoverage' in name):
        return 'Coverage index:<span style="color: green"> &#8593</span>'
    elif('normCrossCorr' in name):
        return 'Cross correlation:<span style="color: green"> &#8593</span>'
    elif('normJaccard' in name):
        return 'Jaccard index:<span style="color: green"> &#8593</span>'
    elif('normDice' in name):
        return 'Dice index:<span style="color: green"> &#8593</span>'
    elif('normCoverage' in name):
        return 'Coverage index:<span style="color: green"> &#8593</span>'
    elif('relMeanRMSMotion' in name):
        return 'Mean value of RMS motion:<span style="color: green"> &#8595</span>'
    elif('relMaxRMSMotion' in name):
        return 'Maximum value of RMS motion:<span style="color: green"> &#8595</span>'
    elif('nSpikesFD' in name):
        return 'Number of spikes per FD:<span style="color: green"> &#8595</span>'
    elif('nspikesDV' in name):
        return 'Number of spikes per DV:<span style="color: green"> &#8595</span>'
    elif('pctSpikesDV' in name):
        return 'Percentage of spikes per DV:<span style="color: green"> &#8595</span>'
    elif('pctSpikesFD' in name):
        return 'Percentage of spikes per DV:<span style="color: green"> &#8595/span>'
    elif('meanDV' in name):
        return 'Mean DVARS:<span style="color: green"> &#8595</span>'
    elif('motionDVCorrInit' in name):
        return 'Correlation of RMS and DVARS before regression:<span style="color: green"> &#8595</span>'
    elif('motionDVCorrFinal' in name):
        return 'Correlation of RMS and DVARS after regression :<span style="color: green"> &#8595 lower than init</span>'
    elif('nNuisanceParameters' in name):
        return 'Total number of nuisance Parameters in addition to custom regressors:<span style="color: green"> &#8595</span> (confound regression model-dependent)'
    elif('nVolCensored' in name):
        return 'Total number of volume(s) censored:<span style="color: green"> &#8595</span>'
    elif('estimatedLostTemporalDOF' in name):
        return 'Total degree of freedom lost:<span style="color: green"> &#8595</span>'
    elif('mean_fd' in name):
        return 'Mean framewise displacement:<span style="color: green"> &#8595</span>'
    elif('max_fd' in name):
        return 'Maximum framewise displacement:<span style="color: green"> &#8595</span>'
    elif('max_translation' in name):
        return '<span style="color: green"> &#8595</span>'
    elif('max_rotation' in name):
        return '<span style="color: green"> &#8595</span>'
    elif('max_rel_translation' in name):
        return 'Maxima of derivative of max_translation:<span style="color: green"> &#8595</span>'
    elif('max_rel_rotation' in name):
        return 'Maxima of derivative of max_rotation:<span style="color: green"> &#8595</span>'
    elif('t1_dice_distance' in name):
        return '<span style="color: green"> &#8593</span>'
    elif('mni_dice_distance' in name):
        return '<span style="color: green"> &#8593</span>'
    elif('raw_incoherence_index ' in name):
        return '<span style="color: green"> &#8595</span>'
    elif('raw_coherence_index ' in name):
        return '<span style="color: green"> &#8593</span>'
    elif('t1_incoherence_index ' in name):
        return '<span style="color: green"> &#8595</span>'
    elif('t1_coherence_index ' in name):
        return '<span style="color: green"> &#8593</span>'
    elif('num_bad_slices' in name):
        return '<span style="color: green"> &#8595</span>'
    elif('raw_dimension' in name):
        return 'Should match protocol field of view'
    elif('raw_voxel_size' in name):
        return 'Should match protocol resolution'
    elif('raw_max_b' in name):
        return 'Should match protocol maximum b'
    elif('raw_neighbor_corr' in name):
        return 'Neighboring DWI Correlation (NDC)'
    elif('raw_num_directions' in name):
        return 'Should match protocol number of directions for dwi scan'
    elif('t1_dimension' in name):
        return 'Preprocessed space field of view'
    elif('t1_voxel_size' in name):
        return 'Preprocessed space resolution controlled by --output_resolution value'
    if('t1_max_b' in name):
        return 'Equal to raw_max_b'
    elif('t1_neighbor_corr' in name):
        return 'Equal to raw_neighbor_corr'
    elif('t1_num_directions' in name):
        return 'Equal to raw_num_directions'
    else:
        return ""
    
    


# In[5]:


def mean(name):
    return str(df[name].mean())


# In[6]:


def median(name):
    return str(df[name].median())


# In[7]:


def std(name):
    return str(df[name].std())


# In[8]:


def rnge(name):
    return str(df[name].max() - df[name].min())


# In[9]:


def outliers(name):
    flag = False
    outs = ""
    mean_ = float(mean(name))
    std_ = float(std(name))
    for i in df.index:
        if((mean_-2*std_)>df[name][i] or df[name][i]>(mean_+2*std_)):
            if(flag):
                outs += ", "+ str(df['subject_id'][i])
                if df['subject_id'][i] in list_outliers:
                    list_outliers[df['subject_id'][i]].append(name)
                else:
                    list_outliers[df['subject_id'][i]] = [name]    
            else:
                outs += str(df['subject_id'][i])
                flag = True
                if df['subject_id'][i] in list_outliers:
                    list_outliers[df['subject_id'][i]].append(name)
                else:
                    list_outliers[df['subject_id'][i]] = [name] 
                
    return outs


# In[17]:


main_name = study_name+"QCGraphs.html"
list_outliers.clear()
f = open(main_name,'w') #create QCGraphs in local folder

grphs = ""
counter = 0
for filename in os.listdir(os.getcwd()):
    if filename.endswith(".png") and filename != "Illini_icon.png":

        #descriptive stats
        name = filename[:len(filename) - 4]
        
        stats = """<table style="width:50% ">
                  <tr>
                    <th colspan="2">"""+name+"""</th>
                  </tr>
                  <tr>
                    <td>Mean</td>
                    <td>"""+mean(name)+"""</td>
                  </tr>
                   <tr>
                    <td>Median</td>
                    <td>"""+median(name)+"""</td>
                  </tr>
                   <tr>
                    <td>Std.</td>
                    <td>"""+std(name)+"""</td>
                  </tr>
                   <tr>
                    <td>Range</td>
                    <td>"""+rnge(name)+"""</td>
                  </tr>
                </table>"""
        
        #create div to align graphs
        if counter%3==0:
            grphs += "<div class=row>"

        grphs+= ("<div class=column><h2 style='text-align:center'>"+name+"</h2><div class='image1'><img src="+ filename+
            " >\n</div><br><p font-style=italic align=center><i>"+stats+ 
            "<br><font size='+2'>" +str(desc(name))+
            "</font><br>Outliers: "+outliers(name)+"</i></p></div>")
        
        if counter % 3==2:
            grphs += "</div>"

        counter+=1
    else:
        continue

code = """<html>
<style>
    body{
        margin:0;
    }
    .row {
        display: flex;
    }
    .column {
        flex: 50%;
        padding: 5px;
    }
    table, th, td {
      border: 1px solid black;
      border-collapse: collapse;
    }
    
    ul {
        list-style-type: none;
        margin: 0;
        padding: 0;
        overflow: hidden;
        background-color: #13294b;
    }

    li {
        float: left;
    }
    li a {
        display: block;
        color: white;
        text-align: center;
        padding: 14px 16px;
        text-decoration: none;
    }
    li a.active {
        background-color: #E84A27;
        color: white;
    }
    li a:hover {
        background-color: #E8E9EA;
    }
    .image1 {
        display: flex;
        justify-content: center;
    }
    
    
    #searchbar{
     padding:13px;
     border-radius: 10px;
   }
 
   input[type=text] {
      width: 7%;
      -webkit-transition: width 0.15s ease-in-out;
      transition: width 0.15s ease-in-out;
   }
   input[type=text]:focus {
     width: 15%;
   }
   
</style>

<head>
<meta name="robots" content="noindex">
    <ul>
        <li><a class="active" href="""+study_name+"""QCGraphs.html>QCGraphs</a></li>
	<li><a href="""+study_name+"""outliers.html>Outliers</a></li>
	<li><a href="""+study_name+"""Anatomical.html>Anatomical</a></li>
        <li><a href="""+study_name+"""ASHS.html>ASHS</a></li>
	<li><a href="""+study_name+"""QSM.html>QSM</a></li>
	<li><a href="""+study_name+"""Diffusion.html>Diffusion</a></li>
	<li><a href="""+study_name+"""GQI.html>GQI</a></li>
	<li><a href="""+study_name+"""CSD.html>CSD</a></li>
	<li><a href="""+study_name+"""NODDI.html>NODDI</a></li>
        <li><a href="""+study_name+"""Functional.html>Functional</a></li>
	<li><a href="""+study_name+"""RSFC.html>RestingState</a></li>
        <li><a href="""+study_name+"""about.html>About</a></li>
        <li style="float:right; padding: 5px;"><img src="Illini_icon.png" width = 3.5% style="float:right"></li>
        <input id="searchbar" onkeyup="Search_var()" type="text" name="search" placeholder="Search...">
    </ul>
     
     
</head>
"""
f.write(code)

#insert graphs
code2 = """

<body style="background-color:#f0f0f0">

<div style = "text-align: center; vertical-align: middle;">
<h1>Last Updated: """+date+"""</h1>
</div>

"""+grphs+"""</body> 

<script>
function Search_var() {
    let input = document.getElementById('searchbar').value
    input=input.toLowerCase();
    let x = document.getElementsByClassName('column');
     
    for (i = 0; i < x.length; i++) {
        if (!x[i].innerHTML.toLowerCase().includes(input)) {
            x[i].style.display="none";
        }
        else {
            x[i].style.display="";                
        }
    }
}
</script>
</html>"""


f.write(code2)
f.close()

#open html file
QCfile = 'file:///'+os.getcwd()+'/' + main_name
webbrowser.open_new_tab(QCfile)


# In[13]:


def get_outliers():
    output = ""
    for key in list_outliers:
        output += "<div class = outliers><br><h2>"+str(key) + "</h2><h3> (" +str(len(list_outliers.get(key)))+" occurences):</h3><br>"
        flag = False
        for item in list_outliers.get(key):
            if flag:
                output += ", "+ str(item)
            else:
                output += str(item)
                flag = True
        output += "</div>"
    return output


# In[14]:


outliers_name = study_name+"outliers.html"
f2 = open(outliers_name,'w') #create outliers in local folder

code = """<html>
<style>
    body{
        margin:0;
    }
    .row {
        display: flex;
    }
    .column {
        flex: 50%;
        padding: 5px;
    }
    table, th, td {
      border: 1px solid black;
      border-collapse: collapse;
    }
    
    ul {
        list-style-type: none;
        margin: 0;
        padding: 0;
        overflow: hidden;
        background-color: #13294b;
    }

    li {
        float: left;
    }
    li a {
        display: block;
        color: white;
        text-align: center;
        padding: 14px 16px;
        text-decoration: none;
    }
    li a.active {
        background-color: #E84A27;
        color: white;
    }
    li a:hover {
        background-color: #E8E9EA;
    }
    .image1 {
        display: flex;
        justify-content: center;
    }
    
    
    #searchbar{
     padding:13px;
     border-radius: 10px;
   }
 
   input[type=text] {
      width: 7%;
      -webkit-transition: width 0.15s ease-in-out;
      transition: width 0.15s ease-in-out;
   }
   input[type=text]:focus {
     width: 15%;
   }
   h2{display:inline;}
   h3{display:inline;}
   
</style>

<head>
<meta name="robots" content="noindex">
    <ul>
        <li><a class="active" href="""+study_name+"""QCGraphs.html>QCGraphs</a></li>
	<li><a href="""+study_name+"""outliers.html>Outliers</a></li>
	<li><a href="""+study_name+"""Anatomical.html>Anatomical</a></li>
        <li><a href="""+study_name+"""ASHS.html>ASHS</a></li>
	<li><a href="""+study_name+"""QSM.html>QSM</a></li>
	<li><a href="""+study_name+"""Diffusion.html>Diffusion</a></li>
	<li><a href="""+study_name+"""GQI.html>GQI</a></li>
	<li><a href="""+study_name+"""CSD.html>CSD</a></li>
	<li><a href="""+study_name+"""NODDI.html>NODDI</a></li>
        <li><a href="""+study_name+"""Functional.html>Functional</a></li>
	<li><a href="""+study_name+"""RSFC.html>RestingState</a></li>
        <li><a href="""+study_name+"""about.html>About</a></li>
        <li style="float:right; padding: 5px;"><img src="Illini_icon.png" width = 3.5% style="float:right"></li>
        <input id="searchbar" onkeyup="Search_var()" type="text" name="search" placeholder="Search...">
    </ul>
    
     
     
</head>
"""
f2.write(code)

#insert outliers
code2 = """

<body style="background-color:#f0f0f0">

<div style = "text-align: center; vertical-align: middle;">
<h1>Last Updated: """+date+"""</h1>
</div>

<div style = "padding:10px">
"""+get_outliers()+"""</div></body> 

<script>
function Search_var() {
    let input = document.getElementById('searchbar').value
    input=input.toLowerCase();
    let x = document.getElementsByClassName('outliers');
     
    for (i = 0; i < x.length; i++) {
        if (!x[i].innerHTML.toLowerCase().includes(input)) {
            x[i].style.display="none";
        }
        else {
            x[i].style.display="";                
        }
    }
}
</script>
</html>"""


f2.write(code2)
f2.close()


about_name = study_name+"about.html"
f3 = open(about_name, 'w')
code = """<html>
<style>
    body{
        margin:0;
    }
    .column {
        flex: 50%;
        padding: 5px;
        }
    ul {
        list-style-type: none;
        margin: 0;
        padding: 0;
        overflow: hidden;
        background-color: #13294b;
    }

    li {
        float: left;
    }
    li a {
        display: block;
        color: white;
        text-align: center;
        padding: 14px 16px;
        text-decoration: none;
    }
    li a.active {
        background-color: #E84A27;
        color: white;
    }
    li a:hover {
        background-color: #E8E9EA;
    }
    .image1 {
        display: flex;
        justify-content: center;
    }
		.about {
		  padding: 40px;
		  text-align: center;
		  background-color: #474e5d;
		  color: white;
		}
	</style>
<head>
<meta name="robots" content="noindex">
    <ul>
        <li><a class="active" href="""+study_name+"""QCGraphs.html>QCGraphs</a></li>
	<li><a href="""+study_name+"""outliers.html>Outliers</a></li>
	<li><a href="""+study_name+"""Anatomical.html>Anatomical</a></li>
        <li><a href="""+study_name+"""ASHS.html>ASHS</a></li>
	<li><a href="""+study_name+"""QSM.html>QSM</a></li>
	<li><a href="""+study_name+"""Diffusion.html>Diffusion</a></li>
	<li><a href="""+study_name+"""GQI.html>GQI</a></li>
	<li><a href="""+study_name+"""CSD.html>CSD</a></li>
	<li><a href="""+study_name+"""NODDI.html>NODDI</a></li>
        <li><a href="""+study_name+"""Functional.html>Functional</a></li>
	<li><a href="""+study_name+"""RSFC.html>RestingState</a></li>
        <li><a href="""+study_name+"""about.html>About</a></li>
        <li style="float:right; padding: 5px;"><img src="Illini_icon.png" width = 3.5% style="float:right"></li>
        <input id="searchbar" onkeyup="Search_var()" type="text" name="search" placeholder="Search...">
    </ul>
</head>

<body style="background-color:#f0f0f0">
	<div class="about">
	  <h1>Quality Control Graphs</h1>
	  <p>Dr. Brad Sutton</p>
	  <p>Paul Camacho</p>
	  <p>Nishant Bhamidipati</p>
	</div>
	
	<div style='text-align:center'>
		<h3>The Quality Control Metrics Graphs provide visual representations of data from the BIC Pipeline. </h3>
		<h3>The subject ID's are listed on the x-axis, while the metric is on the y-axis. Descriptive statistics are included beneath each graph.</h3>
	</div>

</body>

</html>"""

f3.write(code)
f3.close()

modality = "GQI"
page_name = study_name+modality+".html"
fGQI = open(page_name,'w') 

grphs = ""
counter = 0
for filename in os.listdir(os.getcwd()):
    if filename.endswith(".png") and (filename != "Illini_icon.png") and (("gfa" in filename) or ("ncount" in filename) or ("count_end" in filename) or ("count_pass" in filename)):
        #descriptive stats
        name = filename[:len(filename) - 4]
        
        stats = """<table style="width:50% ">
                  <tr>
                    <th colspan="2">"""+name+"""</th>

                  </tr>
                  <tr>
                    <td>Mean</td>
                    <td>"""+mean(name)+"""</td>
                  </tr>
                   <tr>
                    <td>Median</td>
                    <td>"""+median(name)+"""</td>
                  </tr>
                   <tr>
                    <td>Std.</td>
                    <td>"""+std(name)+"""</td>
                  </tr>
                   <tr>
                    <td>Range</td>
                    <td>"""+rnge(name)+"""</td>
                  </tr>
                </table>"""
        
        #create div to align graphs
        if counter%3==0:
            grphs += "<div class=row>"

        grphs+= ("<div class=column><h2 style='text-align:center'>"+name+"</h2><div class='image1'><img src="+ filename+
            " >\n</div><br><p font-style=italic align=center><i>"+stats+ 
            "<br><font size='+2'>" +str(desc(name))+
            "</font><br>Outliers: "+outliers(name)+"</i></p></div>")
        
        if counter % 3==2:
            grphs += "</div>"

        counter+=1
    else:
        continue

code = """<html>
<style>

    body{
        margin:0;
    }
    .row {
        display: flex;
    }
    .column {
        flex: 50%;
        padding: 5px;
    }
    table, th, td {
      border: 1px solid black;
      border-collapse: collapse;
    }
    
    ul {
        list-style-type: none;
        margin: 0;
        padding: 0;
        overflow: hidden;

        background-color: #13294b;
    }

    li {
        float: left;
    }
    li a {
        display: block;
        color: white;
        text-align: center;
        padding: 14px 16px;
        text-decoration: none;
    }
    li a.active {
        background-color: #E84A27;
        color: white;
    }
    li a:hover {

        background-color: #E8E9EA;
    }
    .image1 {
        display: flex;
        justify-content: center;
    }
    
    
    #searchbar{
     padding:13px;
     border-radius: 10px;
   }
 
   input[type=text] {
      width: 7%;
      -webkit-transition: width 0.15s ease-in-out;
      transition: width 0.15s ease-in-out;
   }
   input[type=text]:focus {

     width: 15%;
   }
   
</style>

<head>
<meta name="robots" content="noindex">
    <ul>
        <li><a class="active" href="""+study_name+"""QCGraphs.html>QCGraphs</a></li>
	<li><a href="""+study_name+"""outliers.html>Outliers</a></li>
	<li><a href="""+study_name+"""Anatomical.html>Anatomical</a></li>
        <li><a href="""+study_name+"""ASHS.html>ASHS</a></li>
	<li><a href="""+study_name+"""QSM.html>QSM</a></li>
	<li><a href="""+study_name+"""Diffusion.html>Diffusion</a></li>
	<li><a href="""+study_name+"""GQI.html>GQI</a></li>
	<li><a href="""+study_name+"""CSD.html>CSD</a></li>
	<li><a href="""+study_name+"""NODDI.html>NODDI</a></li>
        <li><a href="""+study_name+"""Functional.html>Functional</a></li>
	<li><a href="""+study_name+"""RSFC.html>RestingState</a></li>
        <li><a href="""+study_name+"""about.html>About</a></li>
        <li style="float:right; padding: 5px;"><img src="Illini_icon.png" width = 3.5% style="float:right"></li>
        <input id="searchbar" onkeyup="Search_var()" type="text" name="search" placeholder="Search...">
    </ul>
    
     
     
</head>
"""
fGQI.write(code)

#insert graphs
codeGQI = """

<body style="background-color:#f0f0f0">

<div style = "text-align: center; vertical-align: middle;">
<h1>Last Updated: """+date+"""</h1>
</div>

"""+grphs+"""</body> 

<script>
function Search_var() {
    let input = document.getElementById('searchbar').value
    input=input.toLowerCase();
    let x = document.getElementsByClassName('column');
     
    for (i = 0; i < x.length; i++) {
        if (!x[i].innerHTML.toLowerCase().includes(input)) {

            x[i].style.display="none";
        }
        else {
            x[i].style.display="";                
        }
    }
}
</script>
</html>"""


fGQI.write(codeGQI)
fGQI.close()

modality = "CSD"
page_name = study_name+modality+".html"
fCSD = open(page_name,'w') 

grphs = ""
counter = 0
for filename in os.listdir(os.getcwd()):
    if filename.endswith(".png") and filename != "Illini_icon.png" and ("SC" in filename):

        #descriptive stats
        name = filename[:len(filename) - 4]
        
        stats = """<table style="width:50% ">
                  <tr>
                    <th colspan="2">"""+name+"""</th>
                  </tr>
                  <tr>
                    <td>Mean</td>
                    <td>"""+mean(name)+"""</td>
                  </tr>
                   <tr>
                    <td>Median</td>
                    <td>"""+median(name)+"""</td>
                  </tr>
                   <tr>
                    <td>Std.</td>
                    <td>"""+std(name)+"""</td>
                  </tr>
                   <tr>
                    <td>Range</td>
                    <td>"""+rnge(name)+"""</td>
                  </tr>
                </table>"""
        
        #create div to align graphs
        if counter%3==0:
            grphs += "<div class=row>"

        grphs+= ("<div class=column><h2 style='text-align:center'>"+name+"</h2><div class='image1'><img src="+ filename+
            " >\n</div><br><p font-style=italic align=center><i>"+stats+ 
            "<br><font size='+2'>" +str(desc(name))+
            "</font><br>Outliers: "+outliers(name)+"</i></p></div>")
        
        if counter % 3==2:
            grphs += "</div>"

        counter+=1
    else:
        continue

code = """<html>
<style>
    body{
        margin:0;
    }
    .row {
        display: flex;
    }
    .column {
        flex: 50%;
        padding: 5px;
    }
    table, th, td {
      border: 1px solid black;
      border-collapse: collapse;
    }
    
    ul {
        list-style-type: none;
        margin: 0;
        padding: 0;
        overflow: hidden;
        background-color: #13294b;
    }

    li {
        float: left;
    }
    li a {
        display: block;
        color: white;
        text-align: center;
        padding: 14px 16px;
        text-decoration: none;
    }
    li a.active {
        background-color: #E84A27;
        color: white;
    }
    li a:hover {
        background-color: #E8E9EA;
    }
    .image1 {
        display: flex;
        justify-content: center;
    }
    
    
    #searchbar{
     padding:13px;
     border-radius: 10px;
   }
 
   input[type=text] {
      width: 7%;
      -webkit-transition: width 0.15s ease-in-out;
      transition: width 0.15s ease-in-out;
   }
   input[type=text]:focus {
     width: 15%;
   }
   
</style>

<head>
<meta name="robots" content="noindex">
    <ul>
        <li><a class="active" href="""+study_name+"""QCGraphs.html>QCGraphs</a></li>
	<li><a href="""+study_name+"""outliers.html>Outliers</a></li>
	<li><a href="""+study_name+"""Anatomical.html>Anatomical</a></li>
        <li><a href="""+study_name+"""ASHS.html>ASHS</a></li>
	<li><a href="""+study_name+"""QSM.html>QSM</a></li>
	<li><a href="""+study_name+"""Diffusion.html>Diffusion</a></li>
	<li><a href="""+study_name+"""GQI.html>GQI</a></li>
	<li><a href="""+study_name+"""CSD.html>CSD</a></li>
	<li><a href="""+study_name+"""NODDI.html>NODDI</a></li>
        <li><a href="""+study_name+"""Functional.html>Functional</a></li>
	<li><a href="""+study_name+"""RSFC.html>RestingState</a></li>
        <li><a href="""+study_name+"""about.html>About</a></li>
        <li style="float:right; padding: 5px;"><img src="Illini_icon.png" width = 3.5% style="float:right"></li>
        <input id="searchbar" onkeyup="Search_var()" type="text" name="search" placeholder="Search...">
    </ul>
    
     
     
</head>
"""
fCSD.write(code)

#insert graphs
codeCSD = """

<body style="background-color:#f0f0f0">

<div style = "text-align: center; vertical-align: middle;">
<h1>Last Updated: """+date+"""</h1>
</div>

"""+grphs+"""</body> 

<script>
function Search_var() {
    let input = document.getElementById('searchbar').value
    input=input.toLowerCase();
    let x = document.getElementsByClassName('column');
     
    for (i = 0; i < x.length; i++) {
        if (!x[i].innerHTML.toLowerCase().includes(input)) {
            x[i].style.display="none";
        }
        else {
            x[i].style.display="";                
        }
    }
}
</script>
</html>"""


fCSD.write(codeCSD)
fCSD.close()

modality = "NODDI"
page_name = study_name+modality+".html"
fNODDI = open(page_name,'w') 

grphs = ""
counter = 0
for filename in os.listdir(os.getcwd()):
    if filename.endswith(".png") and filename != "Illini_icon.png" and ("SC" not in filename) and (("ICVF" in filename) or ("ISOVF" in filename) or ("OD" in filename)):

        #descriptive stats
        name = filename[:len(filename) - 4]
        
        stats = """<table style="width:50% ">
                  <tr>
                    <th colspan="2">"""+name+"""</th>
                  </tr>
                  <tr>
                    <td>Mean</td>
                    <td>"""+mean(name)+"""</td>
                  </tr>
                   <tr>
                    <td>Median</td>
                    <td>"""+median(name)+"""</td>
                  </tr>
                   <tr>
                    <td>Std.</td>
                    <td>"""+std(name)+"""</td>
                  </tr>
                   <tr>
                    <td>Range</td>
                    <td>"""+rnge(name)+"""</td>
                  </tr>
                </table>"""
        
        #create div to align graphs
        if counter%3==0:
            grphs += "<div class=row>"

        grphs+= ("<div class=column><h2 style='text-align:center'>"+name+"</h2><div class='image1'><img src="+ filename+
            " >\n</div><br><p font-style=italic align=center><i>"+stats+ 
            "<br><font size='+2'>" +str(desc(name))+
            "</font><br>Outliers: "+outliers(name)+"</i></p></div>")
        
        if counter % 3==2:
            grphs += "</div>"

        counter+=1
    else:
        continue

code = """<html>
<style>
    body{
        margin:0;
    }
    .row {
        display: flex;
    }
    .column {
        flex: 50%;
        padding: 5px;
    }
    table, th, td {
      border: 1px solid black;
      border-collapse: collapse;
    }
    
    ul {
        list-style-type: none;
        margin: 0;
        padding: 0;
        overflow: hidden;
        background-color: #13294b;
    }

    li {
        float: left;
    }
    li a {
        display: block;
        color: white;
        text-align: center;
        padding: 14px 16px;
        text-decoration: none;
    }
    li a.active {
        background-color: #E84A27;
        color: white;
    }
    li a:hover {
        background-color: #E8E9EA;
    }
    .image1 {
        display: flex;
        justify-content: center;
    }
    
    
    #searchbar{
     padding:13px;
     border-radius: 10px;
   }
 
   input[type=text] {
      width: 7%;
      -webkit-transition: width 0.15s ease-in-out;
      transition: width 0.15s ease-in-out;
   }
   input[type=text]:focus {
     width: 15%;
   }
   
</style>

<head>
<meta name="robots" content="noindex">
    <ul>
        <li><a class="active" href="""+study_name+"""QCGraphs.html>QCGraphs</a></li>
	<li><a href="""+study_name+"""outliers.html>Outliers</a></li>
	<li><a href="""+study_name+"""Anatomical.html>Anatomical</a></li>
        <li><a href="""+study_name+"""ASHS.html>ASHS</a></li>
	<li><a href="""+study_name+"""QSM.html>QSM</a></li>
	<li><a href="""+study_name+"""Diffusion.html>Diffusion</a></li>
	<li><a href="""+study_name+"""GQI.html>GQI</a></li>
	<li><a href="""+study_name+"""CSD.html>CSD</a></li>
	<li><a href="""+study_name+"""NODDI.html>NODDI</a></li>
        <li><a href="""+study_name+"""Functional.html>Functional</a></li>
	<li><a href="""+study_name+"""RSFC.html>RestingState</a></li>
        <li><a href="""+study_name+"""about.html>About</a></li>
        <li style="float:right; padding: 5px;"><img src="Illini_icon.png" width = 3.5% style="float:right"></li>
        <input id="searchbar" onkeyup="Search_var()" type="text" name="search" placeholder="Search...">
    </ul>
    
     
     
</head>
"""
fNODDI.write(code)

#insert graphs
codeNODDI = """

<body style="background-color:#f0f0f0">

<div style = "text-align: center; vertical-align: middle;">
<h1>Last Updated: """+date+"""</h1>
</div>

"""+grphs+"""</body> 

<script>
function Search_var() {
    let input = document.getElementById('searchbar').value
    input=input.toLowerCase();
    let x = document.getElementsByClassName('column');
     
    for (i = 0; i < x.length; i++) {
        if (!x[i].innerHTML.toLowerCase().includes(input)) {
            x[i].style.display="none";
        }
        else {
            x[i].style.display="";                
        }
    }
}
</script>
</html>"""


fNODDI.write(codeNODDI)
fNODDI.close()

modality = "ASHS"
page_name = study_name+modality+".html"
fASHS = open(page_name,'w') 

grphs = ""
counter = 0
for filename in os.listdir(os.getcwd()):
    if filename.endswith(".png") and filename != "Illini_icon.png" and ("_heur" in filename):

        #descriptive stats
        name = filename[:len(filename) - 4]
        
        stats = """<table style="width:50% ">
                  <tr>
                    <th colspan="2">"""+name+"""</th>
                  </tr>
                  <tr>
                    <td>Mean</td>
                    <td>"""+mean(name)+"""</td>
                  </tr>
                   <tr>
                    <td>Median</td>
                    <td>"""+median(name)+"""</td>
                  </tr>
                   <tr>
                    <td>Std.</td>
                    <td>"""+std(name)+"""</td>
                  </tr>
                   <tr>
                    <td>Range</td>
                    <td>"""+rnge(name)+"""</td>
                  </tr>
                </table>"""
        
        #create div to align graphs
        if counter%3==0:
            grphs += "<div class=row>"

        grphs+= ("<div class=column><h2 style='text-align:center'>"+name+"</h2><div class='image1'><img src="+ filename+
            " >\n</div><br><p font-style=italic align=center><i>"+stats+ 
            "<br><font size='+2'>" +str(desc(name))+
            "</font><br>Outliers: "+outliers(name)+"</i></p></div>")
        
        if counter % 3==2:
            grphs += "</div>"

        counter+=1
    else:
        continue

code = """<html>
<style>
    body{
        margin:0;
    }
    .row {
        display: flex;
    }
    .column {
        flex: 50%;
        padding: 5px;
    }
    table, th, td {
      border: 1px solid black;
      border-collapse: collapse;
    }
    
    ul {
        list-style-type: none;
        margin: 0;
        padding: 0;
        overflow: hidden;
        background-color: #13294b;
    }

    li {
        float: left;
    }
    li a {
        display: block;
        color: white;
        text-align: center;
        padding: 14px 16px;
        text-decoration: none;
    }
    li a.active {
        background-color: #E84A27;
        color: white;
    }
    li a:hover {
        background-color: #E8E9EA;
    }
    .image1 {
        display: flex;
        justify-content: center;
    }
    
    
    #searchbar{
     padding:13px;
     border-radius: 10px;
   }
 
   input[type=text] {
      width: 7%;
      -webkit-transition: width 0.15s ease-in-out;
      transition: width 0.15s ease-in-out;
   }
   input[type=text]:focus {
     width: 15%;
   }
   
</style>

<head>
<meta name="robots" content="noindex">
    <ul>
        <li><a class="active" href="""+study_name+"""QCGraphs.html>QCGraphs</a></li>
	<li><a href="""+study_name+"""outliers.html>Outliers</a></li>
	<li><a href="""+study_name+"""Anatomical.html>Anatomical</a></li>
        <li><a href="""+study_name+"""ASHS.html>ASHS</a></li>
	<li><a href="""+study_name+"""QSM.html>QSM</a></li>
	<li><a href="""+study_name+"""Diffusion.html>Diffusion</a></li>
	<li><a href="""+study_name+"""GQI.html>GQI</a></li>
	<li><a href="""+study_name+"""CSD.html>CSD</a></li>
	<li><a href="""+study_name+"""NODDI.html>NODDI</a></li>
        <li><a href="""+study_name+"""Functional.html>Functional</a></li>
	<li><a href="""+study_name+"""RSFC.html>RestingState</a></li>
        <li><a href="""+study_name+"""about.html>About</a></li>
        <li style="float:right; padding: 5px;"><img src="Illini_icon.png" width = 3.5% style="float:right"></li>
        <input id="searchbar" onkeyup="Search_var()" type="text" name="search" placeholder="Search...">
    </ul>
     
     
</head>
"""
fASHS.write(code)

#insert graphs
codeASHS = """

<body style="background-color:#f0f0f0">

<div style = "text-align: center; vertical-align: middle;">
<h1>Last Updated: """+date+"""</h1>
</div>

"""+grphs+"""</body> 

<script>
function Search_var() {
    let input = document.getElementById('searchbar').value
    input=input.toLowerCase();
    let x = document.getElementsByClassName('column');
     
    for (i = 0; i < x.length; i++) {
        if (!x[i].innerHTML.toLowerCase().includes(input)) {
            x[i].style.display="none";
        }
        else {
            x[i].style.display="";                
        }
    }
}
</script>
</html>"""


fASHS.write(codeASHS)
fASHS.close()

modality = "RSFC"
page_name = study_name+modality+".html"
fRSFC = open(page_name,'w') 

grphs = ""
counter = 0
for filename in os.listdir(os.getcwd()):
    if filename.endswith(".png") and filename != "Illini_icon.png" and ("_t1w" and "_pass_" and "_end_" and "area" and "Left" and "Right" and "pass" and "end" and "heur" and "rh" and "lh" and "rec_id" not in filename) and (("36p" in filename) or ("aroma" in filename) or ("despike" in filename) or ("scrub" in filename)):

        #descriptive stats
        name = filename[:len(filename) - 4]
        
        stats = """<table style="width:50% ">
                  <tr>
                    <th colspan="2">"""+name+"""</th>
                  </tr>
                  <tr>
                    <td>Mean</td>
                    <td>"""+mean(name)+"""</td>
                  </tr>
                   <tr>
                    <td>Median</td>
                    <td>"""+median(name)+"""</td>
                  </tr>
                   <tr>
                    <td>Std.</td>
                    <td>"""+std(name)+"""</td>
                  </tr>
                   <tr>
                    <td>Range</td>
                    <td>"""+rnge(name)+"""</td>
                  </tr>
                </table>"""
        
        #create div to align graphs
        if counter%3==0:
            grphs += "<div class=row>"

        grphs+= ("<div class=column><h2 style='text-align:center'>"+name+"</h2><div class='image1'><img src="+ filename+
            " >\n</div><br><p font-style=italic align=center><i>"+stats+ 
            "<br><font size='+2'>" +str(desc(name))+
            "</font><br>Outliers: "+outliers(name)+"</i></p></div>")
        
        if counter % 3==2:
            grphs += "</div>"

        counter+=1
    else:
        continue

code = """<html>
<style>
    body{
        margin:0;
    }
    .row {
        display: flex;
    }
    .column {
        flex: 50%;
        padding: 5px;
    }
    table, th, td {
      border: 1px solid black;
      border-collapse: collapse;
    }
    
    ul {
        list-style-type: none;
        margin: 0;
        padding: 0;
        overflow: hidden;
        background-color: #13294b;
    }

    li {
        float: left;
    }
    li a {
        display: block;
        color: white;
        text-align: center;
        padding: 14px 16px;
        text-decoration: none;
    }
    li a.active {
        background-color: #E84A27;
        color: white;
    }
    li a:hover {
        background-color: #E8E9EA;
    }
    .image1 {
        display: flex;
        justify-content: center;
    }
    
    
    #searchbar{
     padding:13px;
     border-radius: 10px;
   }
 
   input[type=text] {
      width: 7%;
      -webkit-transition: width 0.15s ease-in-out;
      transition: width 0.15s ease-in-out;
   }
   input[type=text]:focus {
     width: 15%;
   }
   
</style>

<head>
<meta name="robots" content="noindex">
    <ul>
        <li><a class="active" href="""+study_name+"""QCGraphs.html>QCGraphs</a></li>
	<li><a href="""+study_name+"""outliers.html>Outliers</a></li>
	<li><a href="""+study_name+"""Anatomical.html>Anatomical</a></li>
        <li><a href="""+study_name+"""ASHS.html>ASHS</a></li>
	<li><a href="""+study_name+"""QSM.html>QSM</a></li>
	<li><a href="""+study_name+"""Diffusion.html>Diffusion</a></li>
	<li><a href="""+study_name+"""GQI.html>GQI</a></li>
	<li><a href="""+study_name+"""CSD.html>CSD</a></li>
	<li><a href="""+study_name+"""NODDI.html>NODDI</a></li>
        <li><a href="""+study_name+"""Functional.html>Functional</a></li>
	<li><a href="""+study_name+"""RSFC.html>RestingState</a></li>
        <li><a href="""+study_name+"""about.html>About</a></li>
        <li style="float:right; padding: 5px;"><img src="Illini_icon.png" width = 3.5% style="float:right"></li>
        <input id="searchbar" onkeyup="Search_var()" type="text" name="search" placeholder="Search...">
    </ul>
     
     
</head>
"""
fRSFC.write(code)

#insert graphs
codeRSFC = """

<body style="background-color:#f0f0f0">

<div style = "text-align: center; vertical-align: middle;">
<h1>Last Updated: """+date+"""</h1>
</div>

"""+grphs+"""</body> 

<script>
function Search_var() {
    let input = document.getElementById('searchbar').value
    input=input.toLowerCase();
    let x = document.getElementsByClassName('column');
     
    for (i = 0; i < x.length; i++) {
        if (!x[i].innerHTML.toLowerCase().includes(input)) {
            x[i].style.display="none";
        }
        else {
            x[i].style.display="";                
        }
    }
}
</script>
</html>"""


fRSFC.write(codeRSFC)
fRSFC.close()

modality = "Anatomical"
page_name = study_name+modality+".html"
fAnat = open(page_name,'w') 

grphs = ""
counter = 0
for filename in os.listdir(os.getcwd()):
    if filename.endswith(".png") and filename != "Illini_icon.png" and ("rest" and "pass" and "end" and "SC" and "aroma" and "despike" and "36p" and "scrub" not in filename) and (("hole" in filename) or ("_t1w" in filename) or ("defect" in filename) or ("topo_" in filename) or ("_snr_orig" in filename) or ("_snr_norm" in filename) or ("cc_size" in filename) or ("_lh_" in filename) or ("_rh_" in filename) or ("rot_tal_" in filename)) and (("qi" in filename) or ("snr" in filename) or ("cnr" in filename) or ("efc" in filename) or ("cjv" in filename) or ("fber" in filename) or ("wm2max" in filename) or ("inu_" in filename) or ("icvs" in filename) or ("rpve" in filename) or ("overlap" in filename) or ("fwhm" in filename)):
        #descriptive stats
        name = filename[:len(filename) - 4]
        
        stats = """<table style="width:50% ">
                  <tr>
                    <th colspan="2">"""+name+"""</th>
                  </tr>
                  <tr>
                    <td>Mean</td>
                    <td>"""+mean(name)+"""</td>
                  </tr>
                   <tr>
                    <td>Median</td>
                    <td>"""+median(name)+"""</td>
                  </tr>
                   <tr>
                    <td>Std.</td>
                    <td>"""+std(name)+"""</td>
                  </tr>
                   <tr>
                    <td>Range</td>
                    <td>"""+rnge(name)+"""</td>
                  </tr>
                </table>"""
        
        #create div to align graphs
        if counter%3==0:
            grphs += "<div class=row>"

        grphs+= ("<div class=column><h2 style='text-align:center'>"+name+"</h2><div class='image1'><img src="+ filename+
            " >\n</div><br><p font-style=italic align=center><i>"+stats+ 
            "<br><font size='+2'>" +str(desc(name))+
            "</font><br>Outliers: "+outliers(name)+"</i></p></div>")
        
        if counter % 3==2:
            grphs += "</div>"

        counter+=1
    else:
        continue

code = """<html>
<style>
    body{
        margin:0;
    }
    .row {
        display: flex;
    }
    .column {
        flex: 50%;
        padding: 5px;
    }
    table, th, td {
      border: 1px solid black;
      border-collapse: collapse;
    }
    
    ul {
        list-style-type: none;
        margin: 0;
        padding: 0;
        overflow: hidden;
        background-color: #13294b;
    }

    li {
        float: left;
    }
    li a {
        display: block;
        color: white;
        text-align: center;
        padding: 14px 16px;
        text-decoration: none;
    }
    li a.active {
        background-color: #E84A27;
        color: white;
    }
    li a:hover {
        background-color: #E8E9EA;
    }
    .image1 {
        display: flex;
        justify-content: center;
    }
    
    
    #searchbar{
     padding:13px;
     border-radius: 10px;
   }
 
   input[type=text] {
      width: 7%;
      -webkit-transition: width 0.15s ease-in-out;
      transition: width 0.15s ease-in-out;
   }
   input[type=text]:focus {
     width: 15%;
   }
   
</style>

<head>
<meta name="robots" content="noindex">
    <ul>
        <li><a class="active" href="""+study_name+"""QCGraphs.html>QCGraphs</a></li>
	<li><a href="""+study_name+"""outliers.html>Outliers</a></li>
	<li><a href="""+study_name+"""Anatomical.html>Anatomical</a></li>
        <li><a href="""+study_name+"""ASHS.html>ASHS</a></li>
	<li><a href="""+study_name+"""QSM.html>QSM</a></li>
	<li><a href="""+study_name+"""Diffusion.html>Diffusion</a></li>
	<li><a href="""+study_name+"""GQI.html>GQI</a></li>
	<li><a href="""+study_name+"""CSD.html>CSD</a></li>
	<li><a href="""+study_name+"""NODDI.html>NODDI</a></li>
        <li><a href="""+study_name+"""Functional.html>Functional</a></li>
	<li><a href="""+study_name+"""RSFC.html>RestingState</a></li>
        <li><a href="""+study_name+"""about.html>About</a></li>
        <li style="float:right; padding: 5px;"><img src="Illini_icon.png" width = 3.5% style="float:right"></li>
        <input id="searchbar" onkeyup="Search_var()" type="text" name="search" placeholder="Search...">
    </ul>
    
     
     
</head>
"""
fAnat.write(code)

#insert graphs
codeAnat = """

<body style="background-color:#f0f0f0">

<div style = "text-align: center; vertical-align: middle;">
<h1>Last Updated: """+date+"""</h1>
</div>

"""+grphs+"""</body> 

<script>
function Search_var() {
    let input = document.getElementById('searchbar').value
    input=input.toLowerCase();
    let x = document.getElementsByClassName('column');
     
    for (i = 0; i < x.length; i++) {
        if (!x[i].innerHTML.toLowerCase().includes(input)) {
            x[i].style.display="none";
        }
        else {
            x[i].style.display="";                
        }
    }
}
</script>
</html>"""


fAnat.write(codeAnat)
fAnat.close()

modality = "Functional"
page_name = study_name+modality+".html"
fFunc = open(page_name,'w') 

grphs = ""
counter = 0
for filename in os.listdir(os.getcwd()):
    if filename.endswith(".png") and filename != "Illini_icon.png" and ("_t1w" and "mean_fd" and "max_fd" and "pass" and "end" and "SC" and "rec_id" and "lh" and "rh" not in filename) and ("_rest" in filename) and (("efc" in filename) or ("fber" in filename) or ("fwhm" in filename) or ("snr" in filename) or ("gcor" in filename) or ("gsr" in filename) or ("fd_" in filename) or ("aor" in filename) or ("aqi" in filename) or ("dummy" in filename)):

        #descriptive stats
        name = filename[:len(filename) - 4]
        
        stats = """<table style="width:50% ">
                  <tr>
                    <th colspan="2">"""+name+"""</th>
                  </tr>
                  <tr>
                    <td>Mean</td>
                    <td>"""+mean(name)+"""</td>
                  </tr>
                   <tr>
                    <td>Median</td>
                    <td>"""+median(name)+"""</td>
                  </tr>
                   <tr>
                    <td>Std.</td>
                    <td>"""+std(name)+"""</td>
                  </tr>
                   <tr>
                    <td>Range</td>
                    <td>"""+rnge(name)+"""</td>
                  </tr>
                </table>"""
        
        #create div to align graphs
        if counter%3==0:
            grphs += "<div class=row>"

        grphs+= ("<div class=column><h2 style='text-align:center'>"+name+"</h2><div class='image1'><img src="+ filename+
            " >\n</div><br><p font-style=italic align=center><i>"+stats+ 
            "<br><font size='+2'>" +str(desc(name))+
            "</font><br>Outliers: "+outliers(name)+"</i></p></div>")
        
        if counter % 3==2:
            grphs += "</div>"

        counter+=1
    else:
        continue

code = """<html>
<style>
    body{
        margin:0;
    }
    .row {
        display: flex;
    }
    .column {
        flex: 50%;
        padding: 5px;
    }
    table, th, td {
      border: 1px solid black;
      border-collapse: collapse;
    }
    
    ul {
        list-style-type: none;
        margin: 0;
        padding: 0;
        overflow: hidden;
        background-color: #13294b;
    }

    li {
        float: left;
    }
    li a {
        display: block;
        color: white;
        text-align: center;
        padding: 14px 16px;
        text-decoration: none;
    }
    li a.active {
        background-color: #E84A27;
        color: white;
    }
    li a:hover {
        background-color: #E8E9EA;
    }
    .image1 {
        display: flex;
        justify-content: center;
    }
    
    
    #searchbar{
     padding:13px;
     border-radius: 10px;
   }
 
   input[type=text] {
      width: 7%;
      -webkit-transition: width 0.15s ease-in-out;
      transition: width 0.15s ease-in-out;
   }
   input[type=text]:focus {
     width: 15%;
   }
   
</style>

<head>
<meta name="robots" content="noindex">
    <ul>
        <li><a class="active" href="""+study_name+"""QCGraphs.html>QCGraphs</a></li>
	<li><a href="""+study_name+"""outliers.html>Outliers</a></li>
	<li><a href="""+study_name+"""Anatomical.html>Anatomical</a></li>
        <li><a href="""+study_name+"""ASHS.html>ASHS</a></li>
	<li><a href="""+study_name+"""QSM.html>QSM</a></li>
	<li><a href="""+study_name+"""Diffusion.html>Diffusion</a></li>
	<li><a href="""+study_name+"""GQI.html>GQI</a></li>
	<li><a href="""+study_name+"""CSD.html>CSD</a></li>
	<li><a href="""+study_name+"""NODDI.html>NODDI</a></li>
        <li><a href="""+study_name+"""Functional.html>Functional</a></li>
	<li><a href="""+study_name+"""RSFC.html>RestingState</a></li>
        <li><a href="""+study_name+"""about.html>About</a></li>
        <li style="float:right; padding: 5px;"><img src="Illini_icon.png" width = 3.5% style="float:right"></li>
        <input id="searchbar" onkeyup="Search_var()" type="text" name="search" placeholder="Search...">
    </ul>
    
     
     
</head>
"""
fFunc.write(code)

#insert graphs
codeFunc = """

<body style="background-color:#f0f0f0">

<div style = "text-align: center; vertical-align: middle;">
<h1>Last Updated: """+date+"""</h1>
</div>

"""+grphs+"""</body> 

<script>
function Search_var() {
    let input = document.getElementById('searchbar').value
    input=input.toLowerCase();
    let x = document.getElementsByClassName('column');
     
    for (i = 0; i < x.length; i++) {
        if (!x[i].innerHTML.toLowerCase().includes(input)) {
            x[i].style.display="none";
        }
        else {
            x[i].style.display="";                
        }
    }
}
</script>
</html>"""


fFunc.write(codeFunc)
fFunc.close()

modality = "Diffusion"
page_name = study_name+modality+".html"
fDIFF = open(page_name,'w') 

grphs = ""
counter = 0
for filename in os.listdir(os.getcwd()):
    if filename.endswith(".png") and filename != "Illini_icon.png" and ("_t1w" and "_pass_" and "_end_" and "area" and "_rest" and "Left" and "Right" and "fc36p" and "aroma" and "despike" and "scrub" and "pass" and "end" and "fber" and "efc" and "fd_mean" and "fwhm" and "gcor" and "holes" and "icvs" and "heur" and "rh" and "lh" and "Init" and "nVol" and "nNuisance" and "normC" and "normD" and "normJ" and "pct" and "qi" and "rec_id" and "RMSM" and "rpve" and "tpm" and "wm2max" and "wm_snr" not in filename) and (("t1_" in filename) or ("mean_fd" in filename) or ("max_fd" in filename) or ("translation" in filename) or ("rel_rotation" in filename)):

        #descriptive stats
        name = filename[:len(filename) - 4]
        
        stats = """<table style="width:50% ">
                  <tr>
                    <th colspan="2">"""+name+"""</th>
                  </tr>
                  <tr>
                    <td>Mean</td>
                    <td>"""+mean(name)+"""</td>
                  </tr>
                   <tr>
                    <td>Median</td>
                    <td>"""+median(name)+"""</td>
                  </tr>
                   <tr>
                    <td>Std.</td>
                    <td>"""+std(name)+"""</td>
                  </tr>
                   <tr>
                    <td>Range</td>
                    <td>"""+rnge(name)+"""</td>
                  </tr>
                </table>"""
        
        #create div to align graphs
        if counter%3==0:
            grphs += "<div class=row>"

        grphs+= ("<div class=column><h2 style='text-align:center'>"+name+"</h2><div class='image1'><img src="+ filename+
            " >\n</div><br><p font-style=italic align=center><i>"+stats+ 
            "<br><font size='+2'>" +str(desc(name))+
            "</font><br>Outliers: "+outliers(name)+"</i></p></div>")
        
        if counter % 3==2:
            grphs += "</div>"

        counter+=1
    else:
        continue

code = """<html>
<style>
    body{
        margin:0;
    }
    .row {
        display: flex;
    }
    .column {
        flex: 50%;
        padding: 5px;
    }
    table, th, td {
      border: 1px solid black;
      border-collapse: collapse;
    }
    
    ul {
        list-style-type: none;
        margin: 0;
        padding: 0;
        overflow: hidden;
        background-color: #13294b;
    }

    li {
        float: left;
    }
    li a {
        display: block;
        color: white;
        text-align: center;
        padding: 14px 16px;
        text-decoration: none;
    }
    li a.active {
        background-color: #E84A27;
        color: white;
    }
    li a:hover {
        background-color: #E8E9EA;
    }
    .image1 {
        display: flex;
        justify-content: center;
    }
    
    
    #searchbar{
     padding:13px;
     border-radius: 10px;
   }
 
   input[type=text] {
      width: 7%;
      -webkit-transition: width 0.15s ease-in-out;
      transition: width 0.15s ease-in-out;
   }
   input[type=text]:focus {
     width: 15%;
   }
   
</style>

<head>
<meta name="robots" content="noindex">
    <ul>
        <li><a class="active" href="""+study_name+"""QCGraphs.html>QCGraphs</a></li>
	<li><a href="""+study_name+"""outliers.html>Outliers</a></li>
	<li><a href="""+study_name+"""Anatomical.html>Anatomical</a></li>
        <li><a href="""+study_name+"""ASHS.html>ASHS</a></li>
	<li><a href="""+study_name+"""QSM.html>QSM</a></li>
	<li><a href="""+study_name+"""Diffusion.html>Diffusion</a></li>
	<li><a href="""+study_name+"""GQI.html>GQI</a></li>
	<li><a href="""+study_name+"""CSD.html>CSD</a></li>
	<li><a href="""+study_name+"""NODDI.html>NODDI</a></li>
        <li><a href="""+study_name+"""Functional.html>Functional</a></li>
	<li><a href="""+study_name+"""RSFC.html>RestingState</a></li>
        <li><a href="""+study_name+"""about.html>About</a></li>
        <li style="float:right; padding: 5px;"><img src="Illini_icon.png" width = 3.5% style="float:right"></li>
        <input id="searchbar" onkeyup="Search_var()" type="text" name="search" placeholder="Search...">
    </ul>
    
     
     
</head>
"""
fDIFF.write(code)

#insert graphs
codeDIFF = """

<body style="background-color:#f0f0f0">

<div style = "text-align: center; vertical-align: middle;">
<h1>Last Updated: """+date+"""</h1>
</div>

"""+grphs+"""</body> 

<script>
function Search_var() {
    let input = document.getElementById('searchbar').value
    input=input.toLowerCase();
    let x = document.getElementsByClassName('column');
     
    for (i = 0; i < x.length; i++) {
        if (!x[i].innerHTML.toLowerCase().includes(input)) {
            x[i].style.display="none";
        }
        else {
            x[i].style.display="";                
        }
    }
}
</script>
</html>"""


fDIFF.write(codeDIFF)
fDIFF.close()


modality = "QSM"
page_name = study_name+modality+".html"
fQSM = open(page_name,'w') 

grphs = ""
counter = 0
for filename in os.listdir(os.getcwd()):
    if filename.endswith(".png") and filename != "Illini_icon.png" and (("ASPIRE_" in filename) or ("OLD_" in filename)):

        #descriptive stats
        name = filename[:len(filename) - 4]
        
        stats = """<table style="width:50% ">
                  <tr>
                    <th colspan="2">"""+name+"""</th>

                  </tr>
                  <tr>
                    <td>Mean</td>
                    <td>"""+mean(name)+"""</td>
                  </tr>
                   <tr>
                    <td>Median</td>
                    <td>"""+median(name)+"""</td>
                  </tr>
                   <tr>
                    <td>Std.</td>
                    <td>"""+std(name)+"""</td>
                  </tr>
                   <tr>
                    <td>Range</td>
                    <td>"""+rnge(name)+"""</td>
                  </tr>
                </table>"""
        
        #create div to align graphs
        if counter%3==0:
            grphs += "<div class=row>"

        grphs+= ("<div class=column><h2 style='text-align:center'>"+name+"</h2><div class='image1'><img src="+ filename+
            " >\n</div><br><p font-style=italic align=center><i>"+stats+ 
            "<br><font size='+2'>" +str(desc(name))+
            "</font><br>Outliers: "+outliers(name)+"</i></p></div>")
        
        if counter % 3==2:
            grphs += "</div>"

        counter+=1
    else:
        continue

code = """<html>
<style>
    body{
        margin:0;

    }
    .row {
        display: flex;
    }
    .column {
        flex: 50%;
        padding: 5px;
    }
    table, th, td {
      border: 1px solid black;
      border-collapse: collapse;
    }
    
    ul {
        list-style-type: none;
        margin: 0;
        padding: 0;
        overflow: hidden;
        background-color: #13294b;
    }

    li {
        float: left;
    }
    li a {
        display: block;
        color: white;

        text-align: center;
        padding: 14px 16px;
        text-decoration: none;
    }
    li a.active {
        background-color: #E84A27;
        color: white;
    }
    li a:hover {
        background-color: #E8E9EA;
    }
    .image1 {
        display: flex;
        justify-content: center;
    }
    
    
    #searchbar{
     padding:13px;
     border-radius: 10px;
   }

 
   input[type=text] {
      width: 7%;
      -webkit-transition: width 0.15s ease-in-out;
      transition: width 0.15s ease-in-out;
   }
   input[type=text]:focus {
     width: 15%;
   }
   
</style>

<head>
<meta name="robots" content="noindex">
    <ul>
        <li><a class="active" href="""+study_name+"""QCGraphs.html>QCGraphs</a></li>
	<li><a href="""+study_name+"""outliers.html>Outliers</a></li>
	<li><a href="""+study_name+"""Anatomical.html>Anatomical</a></li>
        <li><a href="""+study_name+"""ASHS.html>ASHS</a></li>
	<li><a href="""+study_name+"""QSM.html>QSM</a></li>
	<li><a href="""+study_name+"""Diffusion.html>Diffusion</a></li>
	<li><a href="""+study_name+"""GQI.html>GQI</a></li>
	<li><a href="""+study_name+"""CSD.html>CSD</a></li>
	<li><a href="""+study_name+"""NODDI.html>NODDI</a></li>
        <li><a href="""+study_name+"""Functional.html>Functional</a></li>
	<li><a href="""+study_name+"""RSFC.html>RestingState</a></li>
        <li><a href="""+study_name+"""about.html>About</a></li>
        <li style="float:right; padding: 5px;"><img src="Illini_icon.png" width = 3.5% style="float:right"></li>

        <input id="searchbar" onkeyup="Search_var()" type="text" name="search" placeholder="Search...">
    </ul>
    
     
     
</head>
"""
fQSM.write(code)

#insert graphs
codeQSM = """

<body style="background-color:#f0f0f0">


<div style = "text-align: center; vertical-align: middle;">
<h1>Last Updated: """+date+"""</h1>

</div>



"""+grphs+"""</body> 

<script>
function Search_var() {
    let input = document.getElementById('searchbar').value
    input=input.toLowerCase();
    let x = document.getElementsByClassName('column');
     
    for (i = 0; i < x.length; i++) {
        if (!x[i].innerHTML.toLowerCase().includes(input)) {
            x[i].style.display="none";
        }
        else {
            x[i].style.display="";                
        }
    }
}
</script>
</html>"""


fQSM.write(codeQSM)
fQSM.close()
