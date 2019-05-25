#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 21 22:17:42 2019

@author: dryanmiller
"""

def MAESTRO_midi_graph(file_name, plot_type='kdeplot', axis_labels=False, palette='icefire', gridsize=88, figwidth=20, figheight=10):
    from mido import MidiFile
    import seaborn as sns
    import pandas as pd
    import matplotlib.pyplot as plt
    #Import and parse MIDI file using MidiFile from the mido package
    mid = MidiFile(file_name) 
    #Filter the out the meta data in Track 0
    data_list = []
    for i in mid.tracks[1][1:-1]: 
        data_list.append(i)   
    #Transform the MIDI messages to strings
    data_copy = []
    for x in data_list:
        data_copy.append(str(x))
    #Split the message strings into attributes. The first attribute is the message type. Only the value of the message type is provided. The other attributes are listed as keys and values separated by '='.
    result = []
    for message in data_copy:  
        split_str = message.split(" ")
        result.append(split_str)
    #Slice the first attribute (message type) and transform it into a dataframe.
    result2 = []
    for item in result:
        result2.append(item[0])
    df2 = pd.DataFrame(result2)
    #Slice the other attirubtes and store them in a list, one list for each message.
    result3 = []
    for item in result:
        result3.append(item[1:])
    #Transform the attribute lists above into dictionaries. The elements in the attribute list are split into key-value pairs.
    result4 = [{}]    
    for item in result3:
        for i in item:
            key, val = i.split("=")
            if key in result4[-1]:
                result4.append({})
            result4[-1][key] = val
    #Transform the list of dictionaries into a dataframe.
    df3 = pd.DataFrame.from_dict(result4)
    #Rename the series in the first dataframe as 'message_type' and concatenate the two dataframes.
    df2.columns = ['message_type']
    df4 = pd.concat([df2, df3], axis=1)
    #Transform the time attribute from a string to a float
    df4.time = df4.time.astype(float)
    #Engineer a time elapsed attribute equal to the cumulative sum of time.
    df4['time_elapsed'] = df4.time.cumsum()
    #Drop empty and unnecessary attributes
    df4.drop('channel', axis=1, inplace=True)
    try:
        df4.drop('program', axis=1, inplace=True)
    except:
        pass
    #Drop the program_change message. This message occurs only once for these files. The message specifies the instrument to use for playback.
    df4.drop(0, axis=0, inplace=True)
    #Filter out the control_change messages. 
    df5 = df4[df4['message_type']=='note_on']
    df5.note = df5.note.astype(int)
    df5.velocity = df5.velocity.astype(int)
    df5 = df5.loc[df5['velocity'] != 0]

    #df5.velocity = df5.velocity.astype(int)
    if plot_type=='kdeplot':
        sns.set()
        sns.set_style('white')
        fig, ax = plt.subplots(1,1,figsize=(figwidth,figheight))
        g = sns.kdeplot(df5.time_elapsed, df5.note, cmap=palette,
                    shade=True, shade_lowest=True, 
                    vertical=True)
        plt.ylim(min(df5.note), max(df5.note))
        if axis_labels==False:
            ax.set_xlabel('')           
            ax.set_ylabel('')
            g.set(xticklabels='')
            g.set(yticklabels='')
            plt.show();
        else:
            plt.show();
    elif plot_type=='jointplot':
         sns.set_style('white')
         g = sns.jointplot(df5.time_elapsed, df5.note, cmap=palette,
                          kind='hex', xlim=(2,max(df5.time_elapsed)-2), space=0, 
                          joint_kws=dict(gridsize=gridsize))
         g.fig.set_figwidth(figwidth)
         g.fig.set_figheight(figheight)
         if axis_labels==False:
             plt.ylim(min(df5.note), 89)
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
    
  