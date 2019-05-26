def MAESTRO_midi_graph(file_name, plot_type='jointplot', axes_=False, 
                       palette='icefire', gridsize=88, figwidth=20, 
                       figheight=10):
    from mido import MidiFile
    import seaborn as sns
    import pandas as pd
    import matplotlib.pyplot as plt
    #Import and parse MIDI file using MidiFile from the mido package
    mid = MidiFile(file_name) 
    #Filter the out the meta data in Track 0
    message_list = []
    for i in mid.tracks[1][1:-1]: 
        message_list.append(i)   
    #Transform the MIDI messages to strings
    message_strings = []
    for x in message_list:
        message_strings.append(str(x))
    #Split the message strings into attributes. The first attribute is the 
    #message type. Only the value of the message type is provided. The other 
    #attributes are listed as keys and values separated by '='.
    message_strings_split = []
    for message in message_strings:  
        split_str = message.split(" ")
        message_strings_split.append(split_str)
    #Slice the first attribute (message type) and transform it into a dataframe.
    message_type = []
    for item in message_strings_split:
        message_type.append(item[0])
    df1 = pd.DataFrame(message_type)
    df1.columns = ['message_type']
   
    #Slice the other attirubtes and store them in a list, 
    #one list for each message.
    attributes = []
    for item in message_strings_split:
        attributes.append(item[1:])
    #Transform the attribute lists above into dictionaries. 
    #The elements in the attribute list are split into key-value pairs
    #by the = sign.
    attributes_dict = [{}]    
    for item in attributes:
        for i in item:
            key, val = i.split("=")
            if key in attributes_dict[-1]:
                attributes_dict.append({})
            attributes_dict[-1][key] = val
    #Transform the list of dictionaries into a dataframe.
    df2 = pd.DataFrame.from_dict(attributes_dict)
    #Concatenate the two dataframes.
    df_complete = pd.concat([df1, df2], axis=1)
    
    
    #Transform the time and note attributes from strings to floats
    df_complete.time = df_complete.time.astype(float)
    try:
        df_complete.note = df_complete.note.astype(int)
    except:
        pass
    
    #Engineer a time elapsed attribute equal to the cumulative sum of time.
    df_complete['time_elapsed'] = df_complete.time.cumsum()
    
    #Filter rows to include only note_on messages 
    #with a velocity greater than zero
    df_filtered = df_complete[df_complete['message_type']=='note_on']
    df_filtered.note = df_filtered.note.astype(int)
    df_filtered = df_filtered.loc[df_filtered['velocity'] != '0']
    
    #Drop empty and unnecessary attributes
    
    df_filtered.drop(['channel', 'value', 'control', 'time'], 
                     axis=1, inplace=True)
    try:
        df_filtered.drop('program', axis=1, inplace=True)
    except:
        pass
    
    # Add a first and last row. This data is used to improve the plot
    add_first_row = []
    add_first_row.insert(0, {'message_type': 'note_on', 'note': 0, 'time': 0, 
                             'velocity': 0, 
                             'time_elapsed':-df_filtered.iloc[-1]['time_elapsed']*0.05})
    df_final = pd.concat([pd.DataFrame(add_first_row), df_filtered], 
                          ignore_index=True)
    last_time_elapsed = df_final.iloc[-1]['time_elapsed']*1.05
    add_last_row = []
    add_last_row.insert(0, {'message_type': 'note_on', 'note': 127, 'time': 0, 
                            'velocity': 0, 'time_elapsed':last_time_elapsed})
    df_final = pd.concat([df_final, pd.DataFrame(add_last_row)], 
                          ignore_index=True)
    
    # Create plots
    if plot_type=='kdeplot':
        sns.set()
        sns.set_style('white')
        fig, ax = plt.subplots(1,1,figsize=(figwidth,figheight))
        g = sns.kdeplot(df_final.time_elapsed, df_final.note, cmap=palette,
                    shade=True, shade_lowest=True, 
                    vertical=True)
        plt.ylim(16, 113)
        if axes_==False:
            ax.set_xlabel('')           
            ax.set_ylabel('')
            g.set(xticklabels='')
            g.set(yticklabels='')
            plt.axis('off')
            plt.show();
        else:
            plt.show();
    elif plot_type=='jointplot':
        sns.set_style('white')
        g = sns.jointplot(df_final.time_elapsed, df_final.note, cmap=palette,
                          kind='hex', xlim=(min(df_final.time_elapsed),
                                            max(df_final.time_elapsed)), 
                          ylim=(16,113),
                          joint_kws=dict(gridsize=gridsize)
                          )
        if axes_==False:
            sns.despine(left=True, bottom=True) 
            g.fig.set_figwidth(figwidth)
            g.fig.set_figheight(figheight)
            plt.setp(g.ax_marg_x, visible=False)
            plt.setp(g.ax_marg_y, visible=False)
            g.set_axis_labels('', '') 
            plt.setp(g.ax_joint.get_xticklabels(), visible=False)
            plt.setp(g.ax_joint.get_yticklabels(), visible=False)
            plt.show();  
        else:
             plt.show();
    else:
        return "plot_type not allowed"
    
    
  