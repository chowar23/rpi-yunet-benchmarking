####################################################################
# Copyright (C) 2024-2025 Nand Compute LLC | All Rights Reserved 
#
####################################################################

import pandas as pd

MODEL_PI_5 = 'Raspberry Pi 5 Model B Rev 1.0'
MODEL_PI_4 = 'Raspberry Pi 4 Model B Rev 1.1'
MODEL_PI_3 = 'Raspberry Pi 3 Model B Rev 1.2'
MODEL_PI_ZERO_2W = 'Raspberry Pi Zero 2 W Rev 1.0'

MAX_FREQ_PI_5 = 2400
MAX_FREQ_PI_4 = 1500 # w/o boost, 1800 MHz with boost
MAX_FREQ_PI_3 = 1200
MAX_FREQ_PI_ZERO_2W = 1000

OS_BOOKWORM = 'Debian GNU/Linux 12 (bookworm)'

ARCH_64_BIT = 'aarch64'

def read_csv(csv_path):
    '''Read in CSV of previously collected data.'''
    # Read in CSV data to Pandas data frame
    df = pd.read_csv(csv_path)

    # Ensure data types are as exptected
    df['rpi_model']  = df['rpi_model'].astype(str)
    df['os_version'] = df['os_version'].astype(str)
    df['cpu_arch']   = df['cpu_arch'].astype(str)
    df['max_cpu_num']  = df['max_cpu_num'].astype(int)
    df['max_cpu_freq'] = df['max_cpu_freq'].astype(float)
    df['input_width']  = df['input_width'].astype(int)
    df['input_height'] = df['input_height'].astype(int)
    df['model']  = df['model'].astype(str)
    df['inf_ms'] = df['inf_ms'].astype(float)

    return df

def add(df, config, inf_ms):
    '''
    Check to see if data was already collected for this configuration:
      If so, then update with new results.
      If not, then append to end.

    Args:
        df: Pandas data frame of saved data.
        config (dict): Current configuration settings.
        inf_ms (float): Inference time in milliseconds.
    Returns:
        Pandas data frame: Updated data.
    '''
    condition = ( (df['rpi_model']    == config['rpi_model']) & 
                  (df['os_version']   == config['os_version']) & 
                  (df['cpu_arch']     == config['cpu_arch']) & 
                  (df['max_cpu_num']  == config['max_cpu_num']) & 
                  (df['max_cpu_freq'] == config['max_cpu_freq']) &
                  (df['input_width']  == config['input_width']) &
                  (df['input_height'] == config['input_height']) &
                  (df['model']        == config['model']) )

    if len(df[condition]) > 0:
        print('Updating old entry..')
        df.loc[condition, 'inf_ms'] = inf_ms
    elif df.empty == True:
        print('Adding first entry..')
        config['inf_ms'] = inf_ms
        df = pd.DataFrame([config])
    else:
        print('Adding new entry..')
        config['inf_ms'] = inf_ms
        df = pd.concat([df, pd.DataFrame([config])])
    
    return df

def save_to_csv(csv_path, df):
    '''Save data back to CSV file.'''
    df.to_csv(csv_path, index=False)
    
def filter(df, cols, values):
  for idx in range(len(cols)):
    col = cols[idx]
    value = values[idx]
    
    condition = (df[col] == value)
    df = df[condition]
    
  return df

