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
fig_path = '../data/rpi_yunet_cpu_num.jpg'

os_version  = data.OS_BOOKWORM
cpu_arch    = data.ARCH_64_BIT
input_width = 480
input_height = 640

####################################################
# Load data
####################################################
df = data.read_csv(csv_path)

####################################################
# Filter data
####################################################
cols = ['rpi_model', 'os_version', 'cpu_arch', 'max_cpu_freq', 'input_width', 'input_height']
pi5_settings = [data.MODEL_PI_5, os_version, cpu_arch, data.MAX_FREQ_PI_5, input_width, input_height]
pi4_settings = [data.MODEL_PI_4, os_version, cpu_arch, data.MAX_FREQ_PI_4, input_width, input_height]
pi_zero_2w_settings = [data.MODEL_PI_ZERO_2W, os_version, cpu_arch, data.MAX_FREQ_PI_ZERO_2W, input_width, input_height]

pi5_df = data.filter(df.copy(), cols, pi5_settings)
pi5_df = pi5_df.sort_values(by='max_cpu_num')

pi4_df = data.filter(df.copy(), cols, pi4_settings)
pi4_df = pi4_df.sort_values(by='max_cpu_num')

pi_zero_2w_df = data.filter(df.copy(), cols, pi_zero_2w_settings)
pi_zero_2w_df = pi_zero_2w_df.sort_values(by='max_cpu_num')

####################################################
# Plot data
####################################################
plt.figure(1)

x = pi_zero_2w_df['max_cpu_num'].values
y = pi_zero_2w_df['inf_ms'].values
plt.plot(x, y, linestyle='-', marker='.', color='orange')

x = pi4_df['max_cpu_num'].values
y = pi4_df['inf_ms'].values
plt.plot(x, y, linestyle='-', marker='.', color='blue')

x = pi5_df['max_cpu_num'].values
y = pi5_df['inf_ms'].values
plt.plot(x, y, linestyle='-', marker='.', color='red')

plt.gca().invert_xaxis()

plt.legend(['Pi Zero 2W', 'Pi 4', 'Pi 5'])
plt.title('YuNet on Raspberry Pi (Bookworm, 64-bit)')
plt.xlabel('Max CPU Cores')
plt.ylabel('Inference Time [ms]')
plt.grid()

plt.savefig(fig_path)
plt.show()

