from pathlib import Path
import matplotlib as mp
import matplotlib.pyplot as pl
import seaborn as sns
import pandas as pd
import numpy as np
import math


def status(x,i):
    """
    Helper function to get a list of data with contain trip id and other statistical info
    :param x: a column in original dataframe (distance)
    :param i: trip id
    :return: list of data
    """
    curr = []
    for m in x:
        if m>x.quantile(0.25) and m<x.quantile(0.75):
            curr.append(m)

    temp = [i,x.count(), x.min(), x.quantile(.25), x.median(),x.quantile(.75),x.quantile(.9), x.mean(), x.max(), x.mad(), x.var(),x.std(), x.skew(), x.kurt(),str(x.min())+'~'+str(x.max()),x.quantile(0.75)-x.quantile(0.25),np.median(curr)]
    return temp
    # return pd.Series([x.count(), x.min(), x.idxmin(), x.quantile(.25), x.median(),x.quantile(.75), x.mean(), x.max(), x.idxmax(), x.mad(), x.var(),x.std(), x.skew(), x.kurt(),x.quantile(0.75)-x.quantile(0.25),], index=['count', 'min', '0%', '25%','50%', '75%', 'mean', 'max', '100%', 'mean_absolute_deviation', 'variance','standard_deviation', 'skewness', 'unbiased_kurtosis','IQR','IQM'])


def create_table():
    """
    Calculate data and create a dataframe to store them, then write into .csv file
    :return: nothing
    """

    #get the path of the data we need
    p = Path.cwd().parent
    path1 = p / 'Original_Data' / 'sample_99.csv'
    path2 = Path.cwd() / 'complete_data.csv'


    #read data from csv file
    data1 = pd.read_csv(path1)
    data2 = pd.read_csv(path2)

    #create an empty list
    li1 = []
    li2 = []

    #divide data by it's trip_id
    div_data1 = data1.groupby("tripID")
    div_data2 = data2.groupby("tripID")

    #iterative append list data into larger list
    for n, g in div_data1:
        d1 = status(g['distance'],n)
        li1.append(d1)

    #iterative append list data into larger list
    for n, g in div_data2:
        d2 = status(g['angle'],n)
        print(g['angle'])
        li2.append(d2)


    #create a datagrame
    df1 = pd.DataFrame(data=li1,columns=['tripID','count', 'min', '25%','50%', '75%','90%', 'mean', 'max', 'mean_absolute_deviation', 'variance','standard_deviation', 'skewness', 'unbiased_kurtosis','range','IQR','IQM'])
    df2 = pd.DataFrame(data=li2,columns=['tripID','count', 'min', '25%','50%', '75%','90%', 'mean', 'max', 'mean_absolute_deviation', 'variance','standard_deviation', 'skewness', 'unbiased_kurtosis','range','IQR','IQM'])

    #write into .csv file
    df1.to_csv('stat_distance.csv',index=False)
    df2.to_csv('stat_angle.csv',index=False)


def direction():
    """
    Get deviation direction and change column "angle"
    :return: nothing
    """

    # get the path of the data we need
    p = Path.cwd().parent
    path = p / 'Original_Data' / 'sample_99.csv'

    # read data from csv file
    data = pd.read_csv(path)

    li = []

    for x1,x2,y1,y2 in zip(data['origLatitude'],data['correctedLatitude'],data['origLongitude'],data['correctedLongitude']):

        angle = 0.0

        dx = x2 - x1
        dy = y2 - y1

        #check which quadrant the direction is to depend which range the direction angle should be in
        if x2 == x1:
            angle = math.pi / 2.0
            if y2 == y1:
                angle = 0.0
            elif y2 < y1:
                angle = 3.0 * math.pi / 2.0
        elif x2 > x1 and y2 > y1:
            angle = math.atan(dx / dy)
        elif x2 > x1 and y2 < y1:
            angle = math.pi / 2 + math.atan(-dy / dx)
        elif x2 < x1 and y2 < y1:
            angle = math.pi + math.atan(dx / dy)
        elif x2 < x1 and y2 > y1:
            angle = 3.0 * math.pi / 2.0 + math.atan(dy / -dx)

        #append angle to list
        li.append (angle * 180 / math.pi)

    data['angle']=li
    data.to_csv('complete_data.csv')


def visual():
    """
    Visualize overall trip info and seperate trip info
    :return:nothing
    """

    #get current path
    path1 = Path.cwd() / 'Overall_Distance'
    path2 = Path.cwd() / 'By_Trip_Id'

    # read data from csv file
    d = pd.read_csv('complete_data.csv')
    d1 = pd.read_csv('stat_distance.csv')
    odata = d['distance']

    #Fit and plot a univariate or bivariate kernel density estimate of overall distance data
    sns.kdeplot(data=odata)
    pl.savefig(path1 / 'total_kernel_density')

    #Draw a box plot to show distributions with respect to categories of overall distance data
    pl.figure(figsize=(10,100))
    sns.boxplot(data=odata)
    pl.savefig(path1 / 'total_boxplot')

    #Boxplot by trip id
    pl.figure(figsize=(200,50))
    sns.boxplot(x='tripID',y='distance',data=d)
    pl.savefig(path2 / 'trip_box_plot')

    #Lineplot by trip id's statistical info
    pl.figure(figsize=(50,20))
    pl.plot(d1['tripID'],d1['min'],label='Min')
    pl.plot(d1['tripID'],d1['25%'],label='25%')
    pl.plot(d1['tripID'],d1['50%'],label='Median')
    pl.plot(d1['tripID'],d1['75%'],label='75%')
    pl.plot(d1['tripID'],d1['90%'],label='90%')
    pl.plot(d1['tripID'],d1['max'],label='Max')
    pl.plot(d1['tripID'],d1['mean'],label='Mean')

    pl.legend(loc='best')
    pl.savefig(path2 / 'trip_stat_info')

    #Lineplot of other statistical info
    pl.figure(figsize=(50,20))
    pl.plot(d1['tripID'],d1['mean_absolute_deviation'],label='Mean Absolute Seviation')
    pl.plot(d1['tripID'],d1['standard_deviation'],label='Standard Deviation')
    pl.plot(d1['tripID'],d1['skewness'],label='Skewness')
    pl.plot(d1['tripID'],d1['unbiased_kurtosis'],label='Unbiased Kurtosis')
    pl.plot(d1['tripID'],d1['IQR'],label='IQR')
    pl.plot(d1['tripID'],d1['IQM'],label='IQM')

    pl.legend(loc='best')
    pl.savefig(path2 / 'trip_stat_other')

    #Lineplot of variance
    pl.figure(figsize=(50,20))
    pl.plot(d1['tripID'],d1['variance'],label='Variance')

    pl.legend(loc='best')
    pl.savefig(path2 / 'trip_stat_var')

if __name__ == '__main__':
    visual()