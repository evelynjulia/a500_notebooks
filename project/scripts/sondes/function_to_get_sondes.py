#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Eve Wicksteed
#
# 11 December 2019

import glob
import numpy as np
import datetime as dt
import pandas as pd
import os
import matplotlib.pyplot as plt
from scipy import interpolate
import datetime as dt
import seaborn as sns
import pickle


#data_dir = '/Users/catherinemathews/UBC/a500_notebooks/project/data/sondes/'
#fig_dir = '/Users/catherinemathews/UBC/a500_notebooks/project/figures/'

#list_of_files = sorted(glob.glob('/Users/catherinemathews/UBC/a500_notebooks/project/data/sondes/*.csv'))
#list_of_files = glob.glob('/Users/catherinemathews/UBC/a500_notebooks/project/data/sondes/*.csv')

# to get list of files need to get overlapping date list

#top_pres = 850
#stability_limit = 0.005 # what the cutoff is K/mb

def get_sonde_stabilty(data_dir, fig_dir, list_of_files, top_pres, stability_limit):


    """
    Will run and plot sondes, and calculate gradients and stabilty classes
    Plots will have the date they were created (run_date) in the file name
    
    Parameters
    ----------
    data_dir: directory holding sonde files
         e.g. data_dir = '/Users/catherinemathews/UBC/a500_notebooks/project/data/sondes/'

    fig_dir: directory to save figures in

    list_of files: list of files to read in
        should ideally be sorted

    top_pres: the pressure below which I want to get the data

    stability_limit: what the cutoff is (in K/mb) to determine stability
       
    Returns
    -------

    figures:    original_soundings_below_850mb, 
                interpolated_soundings_below_850mb
                stabilty_histograms_below_850mb

                plus 2 seaborn histograms

    pickle files:   sonde_stabilty_classes.pkl
                    sonde_gradients.pkl
    

    """
    
    run_date = dt.datetime.now().strftime('%y%m%d')

    # params / constants
    len_date = 10


    # read all into one dataframe and then groupby date
    fig, ax = plt.subplots(figsize=(15,9))
    

    df_all = pd.DataFrame()
    for file in list_of_files:
        df = pd.read_csv(file, index_col= 'Unnamed: 0')
        date_i = os.path.basename(file)[0:len_date]
        if df.shape[0] > 0:
            # PLOT
            ax.plot(df['THTA'][df['PRES'] > top_pres], df['PRES'][df['PRES'] > top_pres], '.-', label = date_i)

            # get gradient for stability classes:
            df['THTA_GRAD'] = np.gradient(df['THTA'], df['PRES'])
            df['MEAN_GRAD'] = np.mean(df['THTA_GRAD'][df['PRES'] >= top_pres])

            # create column for stability class
            # 0.005 should be about a 0.5 deg C change in temp from 1000mb to 925mb
            stability_conditions = [
                df['THTA_GRAD'][0] >= stability_limit,
                (df['THTA_GRAD'][0] < stability_limit) & (df['THTA_GRAD'][0] > -stability_limit),
                df['THTA_GRAD'][0] <= -stability_limit]
            stability_choices = [-1, 0, 1]  #['unstable', 'neutral', 'stable']
            df['STABILITY'] = np.select(stability_conditions, stability_choices)

            print(df)
            df_all = df_all.append(df)
            print('Adding data for ', date_i)
            print(df_all.shape)

        else: 
            print(date_i,' sounding dataframe is empty... skipping this date/time.')


    ax.set_ylabel('Pressure (mb)')
    ax.set_xlabel('Theta (K)')
    ax.invert_yaxis()
    ax.set_title('Sounding data')
    plt.savefig(fig_dir+'original_soundings_below_850mb_'+run_date+'run.png')


    all_df_pkl_file = open(data_dir+'df_of_all_sondes_orig.pkl', 'wb')
    pickle.dump(df_all, all_df_pkl_file)
    all_df_pkl_file.close()


    # figure 2, 
    p_levs = [1000, 925, 850, 700, 500, 250, 200]

    fig, ax = plt.subplots(figsize=(15,9))


    sonde_stabilty_classes = []
    sonde_gradients = []

    i = 0
    new_df_all = pd.DataFrame()
    for file in list_of_files:
        i += 1
        print('\nnumber of files read = ',i)

        df = pd.read_csv(file, index_col= 'Unnamed: 0')
        date_i = os.path.basename(file)[0:len_date]
        print(date_i)
        hr_i = date_i[-2:]

        new_df_i = pd.DataFrame()
        # now we have the df
        if df.shape[0] > 0:
        
            # get gradient for stability classes:
            df['THTA_GRAD'] = np.gradient(df['THTA'], df['PRES'])
            df['MEAN_GRAD'] = np.mean(df['THTA_GRAD'][df['PRES'] >= top_pres])
            mean_grad_i = np.mean(df['THTA_GRAD'][df['PRES'] >= top_pres])

            # create column for stability class
            # 0.005 should be about a 0.5 deg C change in temp from 1000mb to 925mb
            # calculate stabilty from the 1000mb to 850mb (top_pres) mean
            stability_conditions = [
                df['MEAN_GRAD'][0] >= stability_limit,
                (df['MEAN_GRAD'][0] < stability_limit) & (df['MEAN_GRAD'][0] > -stability_limit),
                df['MEAN_GRAD'][0] <= -stability_limit]
            stability_choices = [-1, 0, 1]  #['unstable', 'neutral', 'stable']
        
            # get interpolations for new columns
            thta_intp = interpolate.interp1d(df['PRES'].values, df['THTA'].values)
            hght_intp = interpolate.interp1d(df['PRES'].values, df['HGHT'].values)
        
            # then add the columns to a new df
            new_df_i['PRES'] = p_levs
            try:
                new_df_i['THTA'] = thta_intp(p_levs)
            except Exception:
                print('broke loop (hopefully)')
                continue
        
            try:
                new_df_i['HGHT'] = hght_intp(p_levs)
            except Exception:
                print('broke loop (hopefully)')
                continue
            new_df_i['DATE'] = df['DATE']
        
            # calc gradient (dtheta_dp)
            # need to make it negative because pressure decreases with height
            new_df_i['THTA_GRAD_INTERP'] = - np.gradient(new_df_i['THTA'], new_df_i['PRES'])
            new_df_i['MEAN_GRAD_INTERP'] = np.mean(new_df_i['THTA_GRAD_INTERP'][new_df_i['PRES'] >= top_pres])

            # set column in new_df_i
            new_df_i['STABILITY'] = np.select(stability_conditions, stability_choices)
            new_df_i['MEAN_GRAD_BELOW_'+str(top_pres)] = mean_grad_i  # mean gradient below 850mb (top_pres), not interpolated

            sonde_stabilty_classes.append(new_df_i['STABILITY'][0])
            sonde_gradients.append(mean_grad_i)

            # column for day / night (Time Of Day)
            tod_conditions = [
                hr_i == '00',
                hr_i == '12']
            tod_choices = [0, 12]  #['night', 'day']
            new_df_i['TOD'] = np.select(tod_conditions, tod_choices)
        
            print(new_df_i)
            ax.plot(new_df_i['THTA'][new_df_i['PRES']>=850], new_df_i['PRES'][new_df_i['PRES']>=850], '.-', label = date_i)

            new_df_all = new_df_all.append(new_df_i)
            print('Adding data for ', date_i)
            print(new_df_all.shape)

        else: 
            print(date_i,'sounding dataframe is empty... skipping this date/time.')
    

    ax.set_ylabel('Pressure (mb)')
    ax.set_xlabel('Theta (K)')
    #plt.legend()
    ax.invert_yaxis()
    ax.set_title('Sounding data')
    #plt.show()
    plt.savefig(fig_dir+'interpolated_soundings_below_850mb_'+run_date+'run.png')


    new_all_df_pkl_file = open(data_dir+'df_of_all_sondes_interp.pkl', 'wb')
    pickle.dump(new_df_all, new_all_df_pkl_file)
    new_all_df_pkl_file.close()

    # stability classes and gradients
    print('stab classes',sonde_stabilty_classes)
    print('gradients',sonde_gradients)

    stab_pkl_file = open(data_dir+'sonde_stabilty_classes.pkl', 'wb')
    pickle.dump(df, stab_pkl_file)
    stab_pkl_file.close()

    grad_pkl_file = open(data_dir+'sonde_gradients.pkl', 'wb')
    pickle.dump(df, grad_pkl_file)
    grad_pkl_file.close()


    fig, ax = plt.subplots(1,2, figsize=(15,9))
    ax[0].hist(sonde_stabilty_classes)
    ax[1].hist(sonde_gradients)
    ax[0].set_xlabel('Stability class')
    ax[1].set_xlabel('Mean gradient between 1000mb and 850mb')
    plt.savefig(fig_dir+'stabilty_histograms_below_850mb_'+run_date+'run.png')

    # fig, ax = plt.subplots(figsize=(15,9))
    # sns.distplot(sonde_stabilty_classes)
    # #ax.set_xlabel('Stability class')
    # fig.set_axis_labels('Stability class')
    # plt.savefig(fig_dir+'sns_stab_hist_below_850mb_'+run_date+'run.png')

    # #fig, ax = plt.subplots(figsize=(15,9))
    # p = sns.distplot(sonde_gradients)
    # p = p.set_axis_labels('Mean gradient between 1000mb and 850mb', '')
    # #ax.set_xlabel('Mean gradient between 1000mb and 850mb')
    # plt.title("title")
    # plt.savefig(fig_dir+'sns_grad_hist_below_850mb_'+run_date+'run.png')

    j = sns.distplot(sonde_stabilty_classes)
    #j.annotate(stats.pearsonr)
    j.fig.set_size_inches(8,8)
    j.fig.suptitle('Stability class')
    j.savefig(fig_dir+'sns_stab_hist_below_850mb_'+run_date+'run.png')


    return




