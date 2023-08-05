# -*- coding: utf-8 -*-
"""
Created on Tue Aug  9 14:50:37 2022

@author: Mufti Mubashir
https://datagy.io/split-pandas-dataframe/
"""
import pandas as pd

def split_dataframe_by_position(df, splits):
    """
    Takes a dataframe and an integer of the number of splits to create.
    Returns a list of dataframes.
    """
    dataframes = []
    index_to_split = len(df) // splits
    start = 0
    end = index_to_split
    for split in range(splits):
        temporary_df = df.iloc[start:end, :]
        dataframes.append(temporary_df)
        start += index_to_split
        end += index_to_split
    return dataframes

df = pd.read_csv("dataset/full/month_74_77_clean.csv")

total_parts = 10
part_of_total =1
 
split_dataframes = split_dataframe_by_position(df, total_parts)
print(split_dataframes[part_of_total])

split_dataframes[part_of_total].to_csv('dataset/sample/' + str(part_of_total)+ 'by' + str(total_parts)+'.csv')