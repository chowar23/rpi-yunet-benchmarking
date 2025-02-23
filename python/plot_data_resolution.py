####################################################################
# Copyright (C) 2024-2025 Nand Compute LLC | All Rights Reserved 
#
####################################################################

import matplotlib.pyplot as plt
import pandas as pd

import data

####################################################
# Constants
####################################################
csv_path = '../data/rpi_yunet_data.csv'
fig_path = '../data/rpi_yunet_resolution.jpg'

os_version  = data.OS_BOOKWORM
cpu_arch    = data.ARCH_64_BIT
max_cpu_num = 4

####################################################
# Load data
####################################################
df = data.read_csv(csv_path)

####################################################
# Filter data
####################################################
cols = ['rpi_model', 'os_version', 'cpu_arch', 'max_cpu_num', 'max_cpu_freq']
pi5_settings = [data.MODEL_PI_5, os_version, cpu_arch, max_cpu_num, data.MAX_FREQ_PI_5]
pi4_settings = [data.MODEL_PI_4, os_version, cpu_arch, max_cpu_num, data.MAX_FREQ_PI_4]
pi3_settings = [data.MODEL_PI_3, os_version, cpu_arch, max_cpu_num, data.MAX_FREQ_PI_3]
pi_zero_2w_settings = [data.MODEL_PI_ZERO_2W, os_version, cpu_arch, max_cpu_num, data.MAX_FREQ_PI_ZERO_2W]

pi5_df = data.filter(df.copy(), cols, pi5_settings)
pi5_df = pi5_df.sort_values(by='input_width')

pi4_df = data.filter(df.copy(), cols, pi4_settings)
pi4_df = pi4_df.sort_values(by='input_width')

pi3_df = data.filter(df.copy(), cols, pi3_settings)
pi3_df = pi3_df.sort_values(by='input_width')

pi_zero_2w_df = data.filter(df.copy(), cols, pi_zero_2w_settings)
pi_zero_2w_df = pi_zero_2w_df.sort_values(by='input_width')

####################################################
# Plot data
####################################################
plt.figure(1)

x = pi3_df['input_width'].values * pi3_df['input_height'].values
y = pi3_df['inf_ms'].values
plt.plot(x, y, linestyle='-', marker='.', color='green')

x = pi_zero_2w_df['input_width'].values * pi_zero_2w_df['input_height'].values
y = pi_zero_2w_df['inf_ms'].values
plt.plot(x, y, linestyle='-', marker='.', color='orange')

x = pi4_df['input_width'].values * pi4_df['input_height'].values
y = pi4_df['inf_ms'].values
plt.plot(x, y, linestyle='-', marker='.', color='blue')

x = pi5_df['input_width'].values * pi5_df['input_height'].values
y = pi5_df['inf_ms'].values
plt.plot(x, y, linestyle='-', marker='.', color='red')

plt.xscale('log')
plt.xticks(ticks=[640*480, 320*240, 160*120, 80*60], 
           labels=['480x640', '240x320', '120x160', '60x80'],
           rotation=0)
plt.gca().invert_xaxis()


plt.legend(['Pi 3', 'Pi Zero 2W', 'Pi 4', 'Pi 5'])
plt.title('YuNet on Raspberry Pi (Bookworm, 64-bit)')
plt.xlabel('Resolution')
plt.ylabel('Inference Time [ms]')
plt.grid()

plt.savefig(fig_path)
plt.show()

