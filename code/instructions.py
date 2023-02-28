import dash_bootstrap_components as dbc
from dash import dcc, html, dash_table
import dash_player as dp

video_path = 'assets/test.mp4'

'''dbc.Button('Instructions', id='instruction-button'),
        dbc.Collapse(dbc.Card(dbc.CardBody([
            html.P('1. Create an excel or csv file with headers shown in the template below or download the template using the export button'),
            #
            dash_table.DataTable(data=poi_template.to_dict('records'),
                        columns=[{"name": i, "id": i} for i in poi_template.columns],
                        export_format="csv",
                        export_headers="display",
                        style_table={'overflowX': 'auto',},
                        style_cell={'whiteSpace': 'normal',},),
            html.P('2. Fill in the IDs, must match with the ones in your processed data (table in above section)'),
            html.P('3. The start and end time of the period must be in the format DD/MM/YY HH:MM'),
            html.P('4. Add a label if you\'d like to'),
            html.P('5 Add an optional set period to look at the window after your period of interest'),
        ])), id='instructions-collapse'),'''

layout = html.Div([
    html.H1('Documentation'),
    dbc.Card(dbc.CardBody([
        dbc.Accordion([
            dbc.AccordionItem([
                dbc.Row([
                    dbc.Col(
                        html.P('The Diametrics dashboard is navigated using the tabs at the top of the page. The first 4 tabs must be run consecutively, and you won’t be able to open the next one before the previous one is completed. The final 2 tabs can be accessed once the standard metrics in tab 4 have been calculated. For a more detailed description of each tab see the description below.'),
                    ),
                    dbc.Col(
                        dp.DashPlayer(url='https://www.youtube.com/watch?v=dOphbyjhACM', controls=True),
                    )
                ])
            ], title='Changing tabs'),
            dbc.AccordionItem([
                dp.DashPlayer(url='https://youtu.be/d5pb9TgCGc0', controls=True),
                dbc.Row([
                    dbc.Col(
                        html.P('To upload data either select or drag and drop your CGM files into the dashed box. Currently, the filetypes we accept are csv, excel or text. There is no upper limit to the size of the file or the number of files you upload. You may run into problems if the total size of all your files is more than what the browser can handle. \
                            The app will detect automatically whether the glucose data for each file is in mmol/L or mg/dL. It cannot, however, determine whether the datetime is written in European or American format. It is therefore assumed that it is in European (DD/MM/YYYY).\
                                The filename will be used to create a unique ID for each CGM file so ensure that the names are intuitive and unique.\
                                Once the upload is complete, you’ll find a list of files underneath for you to double check that the files you’ve uploaded are correct. ')
                    ), 
                    dbc.Col(
                        dp.DashPlayer(url='https://youtu.be/d5pb9TgCGc0', controls=True),
                    )
                ])
            ], title='Uploading data'),
            dbc.AccordionItem([
                dcc.Markdown('This section serves to give you an overview of the processed CGM files you uploaded and allows you to do some minor editing of the data. To get more information about each column, hover over the column name. \
                        If the data is not usable, you will see the **Usable** column says No and the row is highlighted red. If the row is highlighted red in any case, it means that the analysis with this file cannot go any further \
                        and you will need to edit your file in some way. To better understand why your file isn’t working you can use the to list below to help you debug the potential cause of the error:')
            ], title='Data overview'),
            dbc.AccordionItem([
                dcc.Markdown('''This section is completely optional. If you’d like to stick with the standard metrics of glycemic control outlined in the International Consensus, then just press the next button to continue. \
If you’d like to have a biThis section is completely optional. If you’d like to stick with the standard metrics of glycemic control outlined in the International Consensus, then just press the next button to continue. \
If you’d like to have a bit more control over how your metrics are calculated, there are three different ways you can do that here. If there’s any additional options you’d like to see, please get in contact! \
### Day/night time
You can edit the day/night settings by clicking on the first drop-down bar. Here you can enter the times for the start and end of the day and night-time. The default times are set to 6am-12am for the day and 12am-6am for the night, as defined in the International Consensus. \
The times you set don’t need to be the same for day and night, for example you can finish the day at 10pm and start the night at 2am (or vice versa). However, the times you set will remain the same across all files, at this stage you can’t tailor them to individuals. If you’re interested in more in-depth periodic analysis, then see the advanced analysis section.\
### Time in range thresholds
The International Consensus suggests the calculate the percentage time in the following standard ranges:\
              * Time in normal range (3.9-10.0 mmol/L)\
      * Time in level 1 hypoglycemia (3.0-3.9 mmol/L)\
      * Time in level 2 hypoglycemia (<3.0 mmol/L)\
      * Time in level 1 hyperglycemia (10.0-13.9 mmol/L)\
      * Time in level 2 hyperglycemia (>13.9 mmol/L)\
If you’re interested in looking at the percentage of time spent in a range that’s outside of the standard ranges (see below), you can add a threshold by clicking the **Add another range** button. You can then drag the lower and higher thresholds to select the range you’re interested in. This will then appear in your standard metrics on the following tab with the header **Time in range (lower threshold)-(upper threshold) mmol/L**.\
If you want to add a < or > threshold, just set the other thresholds to either the lowest or highest point on the slider, respectively.\
If you want to remove a time in range threshold, click the **Remove** button next to the range you want to delete.\
For now, the sliders are only in mmol/L and aren’t available in mg/dL.\
### Glycemic events
The International consensus defines a glycemic event as 15 minutes or more below/above the level 1 threshold (3.9 and 10.0mmol/L for hypo/hyper-glycemia, respectively). The episode is over when 15 mins are spent back under/over the threshold. A level 2 event is reached when the glucose level drops below/above the level 2 threshold (3.0 and 13.9 mmol/L for hypo/hyper-glycemia respectively) for 15 minutes. A prolonged episode is 120 mins consecutively spent in level 2 hypo/hyper-glycemia.\
If you’d like to change these defaults, you can use the sliders to adjust the thresholds for level 1 and level 2 episodes for both hypoglycemia (middle panel) and hyperglycemia (right panel). To change the duration of episodes, edit the number of minutes for regular and prolonged events (left panel).')t more control over how your metrics are calculated, there are three different ways you can do that here. If there’s any additional options you’d like to see, please get in contact!\
You can edit the day/night settings by clicking on the first drop-down bar. Here you can enter the times for the start and end of the day and night-time. The default times are set to 6am-12am for the day and 12am-6am for the night, as defined in the International Consensus. \
The times you set don’t need to be the same for day and night, for example you can finish the day at 10pm and start the night at 2am (or vice versa). However, the times you set will remain the same across all files, at this stage you can’t tailor them to individuals. If you’re interested in more in-depth periodic analysis, then see the advanced analysis section.\

### Time in range thresholds
The International Consensus suggests the calculate the percentage time in the following standard ranges:\
    * Time in normal range (3.9-10.0 mmol/L)\
      * Time in level 1 hypoglycemia (3.0-3.9 mmol/L)\
      * Time in level 2 hypoglycemia (<3.0 mmol/L)\
      * Time in level 1 hyperglycemia (10.0-13.9 mmol/L)\
      * Time in level 2 hyperglycemia (>13.9 mmol/L)\
If you’re interested in looking at the percentage of time spent in a range that’s outside of the standard ranges (see below), you can add a threshold by clicking the **Add another range** button. You can then drag the lower and higher thresholds to select the range you’re interested in. This will then appear in your standard metrics on the following tab with the header **Time in range (lower threshold)-(upper threshold) mmol/L**.\
If you want to add a < or > threshold, just set the other thresholds to either the lowest or highest point on the slider, respectively.\
If you want to remove a time in range threshold, click the **Remove** button next to the range you want to delete.\
For now, the sliders are only in mmol/L and aren’t available in mg/dL.\
### Glycemic events\
The International consensus defines a glycemic event as 15 minutes or more below/above the level 1 threshold (3.9 and 10.0mmol/L for hypo/hyper-glycemia, respectively). The episode is over when 15 mins are spent back under/over the threshold. A level 2 event is reached when the glucose level drops below/above the level 2 threshold (3.0 and 13.9 mmol/L for hypo/hyper-glycemia respectively) for 15 minutes. A prolonged episode is 120 mins consecutively spent in level 2 hypo/hyper-glycemia.\
If you’d like to change these defaults, you can use the sliders to adjust the thresholds for level 1 and level 2 episodes for both hypoglycemia (middle panel) and hyperglycemia (right panel). To change the duration of episodes, edit the number of minutes for regular and prolonged events (left panel).''')
            ], title='Analysis options'),
            dbc.AccordionItem([
                html.P('')
            ], title=''),
            dbc.AccordionItem([
                html.P('')
            ], title=''),
        ], start_collapsed=True),
    
                                
                                dcc.Markdown(['''
                                # Diametrics documentation
## Dashboard
### Overview
Talk about the international consensus

### Changing tabs
The Diametrics dashboard is navigated using the tabs at the top of the page. The first 4 tabs must be run consecutively, and you won’t be able to open the next one before the previous one is completed. The final 2 tabs can be accessed once the standard metrics in tab 4 have been calculated. For a more detailed description of each tab see the description below.

### Uploading data
To upload data either select or drag and drop your CGM files into the dashed box. Currently, the filetypes we accept are csv, excel or text. There is no upper limit to the size of the file or the number of files you upload. You may run into problems if the total size of all your files is more than what the browser can handle. 
The app will detect automatically whether the glucose data for each file is in mmol/L or mg/dL. It cannot, however, determine whether the datetime is written in European or American format. It is therefore assumed that it is in European (DD/MM/YYYY).
The filename will be used to create a unique ID for each CGM file so ensure that the names are intuitive and unique.
Once the upload is complete, you’ll find a list of files underneath for you to double check that the files you’ve uploaded are correct. 

### Data overview
This section serves to give you an overview of the processed CGM files you uploaded and allows you to do some minor editing of the data. To get more information about each column, hover over the column name. 
If the data is not usable, you will see the usable column says No and the row is highlighted red. If the row is highlighted red in any case, it means that the analysis with this file cannot go any further and you will need to edit your file in some way. To better understand why your file isn’t working you can use the debugger to explore the potential cause of the error.
The Start DateTime and End DateTime columns can be edited to adjust the period you want to analyse. The format for this will need to be either YYYY-MM-DD HH:MM or YYYY/MM/DD HH:MM. If edited, the Days and Data Sufficiency (%) columns will be updated automatically. If the entries are invalid, you’ll see N/A appear and the row will be highlighted red to show that it is no longer usable. The International consensus specifies that there should be a minimum of 2 weeks of data with 70-80% data sufficiency. If either the number of days or the data sufficiency are below this recommendation, they will be highlighted orange to let you know but you can still continue with your analysis.
The two devices that have been hardcoded into the program are Libre and Dexcom. This will show in the Device column. An autoprocessing tool has been added to process files that don’t fit into these formats however this will not work on all data. If the data has been autoprocessed then the device type will show as Unknown.
Analysis options
This section is completely optional. If you’d like to stick with the standard metrics of glycemic control outlined in the International Consensus, then just press the next button to continue. 
If you’d like to have a bit more control over how your metrics are calculated, there are three different ways you can do that here. If there’s any additional options you’d like to see, please get in contact!
#### Day/night time
You can edit the day/night settings by clicking on the first drop-down bar. Here you can enter the times for the start and end of the day and night-time. The default times are set to 6am-12am for the day and 12am-6am for the night, as defined in the International Consensus. 
The times you set don’t need to be the same for day and night, for example you can finish the day at 10pm and start the night at 2am (or vice versa). However, the times you set will remain the same across all files, at this stage you can’t tailor them to individuals. If you’re interested in more in-depth periodic analysis, then see the advanced analysis section.
#### Time in range thresholds
The International Consensus suggests the calculate the percentage time in the following standard ranges:
    * Time in normal range (3.9-10.0 mmol/L)
    * Time in level 1 hypoglycemia (3.0-3.9 mmol/L)
    * Time in level 2 hypoglycemia (<3.0 mmol/L)
    * Time in level 1 hyperglycemia (10.0-13.9 mmol/L)
    * Time in level 2 hyperglycemia (>13.9 mmol/L)
If you’re interested in looking at the percentage of time spent in a range that’s outside of the standard ranges (see below), you can add a threshold by clicking the Add another range button. You can then drag the lower and higher thresholds to select the range you’re interested in. This will then appear in your standard metrics on the following tab with the header Time in range (lower threshold)-(upper threshold) mmol/L.
If you want to add a < or > threshold, just set the other thresholds to either the lowest or highest point on the slider, respectively.
If you want to remove a time in range threshold, click the Remove button next to the range you want to delete.
For now, the sliders are only in mmol/L and aren’t available in mg/dL.
#### Glycemic events
The International consensus defines a glycemic event as 15 minutes or more below/above the level 1 threshold (3.9 and 10.0mmol/L for hypo/hyper-glycemia, respectively). The episode is over when 15 mins are spent back under/over the threshold. A level 2 event is reached when the glucose level drops below/above the level 2 threshold (3.0 and 13.9 mmol/L for hypo/hyper-glycemia respectively) for 15 minutes. A prolonged episode is 120 mins consecutively spent in level 2 hypo/hyper-glycemia.
If you’d like to change these defaults, you can use the sliders to adjust the thresholds for level 1 and level 2 episodes for both hypoglycemia (middle panel) and hyperglycemia (right panel). To change the duration of episodes, edit the number of minutes for regular and prolonged events (left panel).

### Standard metrics
This tab shows you all of the metrics of glycemic control recommended by the International Consensus. If you hover over the headings you will find the long version for any acronyms. To get a more detailed description of how the all the metrics are calculated, please go our GitHub where you can also find all the open source code.
At the top of the tab, there are two sets of buttons. The first will change the units from mmol/L to mg/dL. The second set gives you a breakdown of the metrics for day and night times selected in the analysis options section. You can see the times that are being used below the buttons.
You can sort or filter the rows based by specific columns. You can also hide columns by pressing the eye button to the left of the column name. If you want the columns back again you can click on the Toggle Columns button to select and deselect the ones you want in the table.
To download the table, click the Export button. Be aware, it will download the table exactly as it looks on the screen so all of the filtering, sorting and column toggling you do will be in your final file.
Below the table are two overview data visualisations. The first is a bar graph that shows the result of each metric for each individual. The default is set to time in range, broken down into the different ranges recommended by the International Consensus. The second visualisation in a boxplot to show the distribution of the metric between individuals in the data uploaded. Both of these visualisations are controlled with the dropdown selection to the right of the page. These figures reflect the data in the table, so will change when units or time period is changed with the buttons at the top.

### Visualisations
The visualisations tab contains three figures that explore each CGM file uploaded. The ID can be changed with the dropdown bar at the top. All figures can be downloaded and manipulated using the toolbar at the top right of each figure. Hover over the icons to see what each one does.
The first figure is the ambulatory glucose profile. Essentially, it’s an average 24-hour period taken over the period you’ve given. The yellow central line shows the median glucose, the blue shows the interquartile range (25th and 75th percentiles) and the green dashed lines show the 10th and 90th percentiles. The second figure is a pie chart with the breakdown of the standard percentage time in ranges. The final figure is a line graph of the entire glucose trace.
Advanced analysis
This section enables you to take a more in depth look at different periods of interest in your data. For this to work you'll need to upload a file that includes the ID of the participant, the start and end times of the period of interest and an optional label. From there, you'll get a breakdown of the metrics of glycemic control for all of the periods you've entered.

### Upload external data
You need to upload a file that specifies the periods you are interested in. This can be either an excel or csv file.
The file can be in a few different formats, but it’s essential that you match the column names up perfectly to the ones described below.
ID
There needs to be an ID column in your file, and this must exactly match an ID from the files you uploaded in the first section. So if you uploaded a file called ‘trialX_P03.csv’, then the ID you would need to put in is ‘trialX_P03’. 
Start and end time
We need to know the start and end time of the period so we need the start date and time, and either the end date and time or the duration.
The following combinations are your options:
    * startDateTime, endDateTime
    * ID, startDate, startTime, endDate, endTime, label
    * ID, startDateTime, duration, label
    * ID, startDate, startTime, duration, label
The date entries need to be in the following formats:
    * YYYY-MM-DD
    * YYYY/MM/DD
    * DD-MM-YYYY
    * DD/MM/YYYY
Time entries should be HH:MM or HH:MM:SS
Datetime is one of the date entries plus the time entry, e.g. YYYY-MM-DD HH:MM
Duration need to be the number of minutes.
Label(s)
Labels are optional. You can use them to distinguish the periods you’re interested in. You can have as many labels as you like and you can call them whatever you like. In the examples we will call them ‘label’ and ‘label2’ for simplicity.



Select the periods of interest
This part allows you to look at the windows around the event. This is going to be particularly useful if you’re establishing someone’s glycemic control during set periods, for example exercise and the 4 hours after exercise. The two boxes tick boxes let you choose if you want to see the standard metrics for the whole 24 hours after the period of interest and if you want to see the night after the event. The night-time is taken from the analysis options in tab 3 (default 12am-6am).
The range sliders below give you the chance to customise the window you are interested in around the periods you’ve entered. The first slider is set to the default window of the start of the period to the end of the period. Leave this one as it is if you want to keep this in your analysis. You can add new windows by clicking the Add another window button and select the range you’re interested in. Currently, you can only add windows up to 4 hours before and after the event. The time before is measured from the start of the event and the time after is measured from the end.
Calculate metrics
Click the Calculate metrics button and wait for your metrics to be calculated. This will show all of the metrics of glycemic control for each period you’ve specified. Any changes you made in the analysis options will also be in these reflected in these metrics.
The different periods can be identified by the ID, the start date and time, and the optional labels.
Above the metrics table is the button to change the units from mmol/L to mg/dL. You can sort or filter the rows based by specific columns. You can also hide columns by pressing the eye button to the left of the column name. If you want the columns back again you can click on the Toggle Columns button to select and deselect the ones you want in the table.
To download the table, click the Export button. Be aware, it will download the table exactly as it looks on the screen so all of the filtering, sorting and column toggling you do will be in your final file.
                                '''])
]))])