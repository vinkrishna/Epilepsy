#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 00:25:40 2023

@author: vkumar
"""
import os
os.chdir('/Users/vkumar/Documents/Writings/Pascal')

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import ptitprince as pt

# Read the CSV file with comma as decimal separator
data = pd.read_csv("data_thalamus.csv", sep=';', decimal=',')

# Separate the data into two groups: controls (0) and patients (1)
controls = data[data["Group"] == 0]
patients = data[data["Group"] == 1]

# Get the structure names (starting from the 3rd column)
structure_names = data.columns[2:]

# Perform a t-test for each structure and create a raincloud plot
for structure in structure_names:
    control_volumes = controls[structure]
    patient_volumes = patients[structure]

    # Perform the t-test
    t_stat, p_value = stats.ttest_ind(control_volumes, patient_volumes)

    # Prepare data for the raincloud plot
    combined_data = pd.concat([control_volumes, patient_volumes], axis=0)
    group_labels = ['Controls'] * len(control_volumes) + ['Patients'] * len(patient_volumes)
    plot_data = pd.DataFrame({'Group': group_labels, 'Volume': combined_data, 'Structure': [structure] * len(combined_data)})

    # Create a raincloud plot
    plt.figure(figsize=(6, 6))
    pt.RainCloud(x='Group', y='Volume', data=plot_data, width_viol=.6, width_box=.2, orient='h')
    plt.title(f"{structure} Volumes (p = {p_value:.4f})")
    plt.savefig(f"{structure}_Volumes.png", dpi=300, bbox_inches='tight')
    plt.show()

    # Check if the comparison is significant (p < 0.05)
    if p_value < 0.05:
        print(f"The difference in {structure} volumes between controls and patients is significant (p = {p_value:.4f}).")
    else:
        print(f"The difference in {structure} volumes between controls and patients is not significant (p = {p_value:.4f}).")
