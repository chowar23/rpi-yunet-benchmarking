####################################################################
# Copyright (C) 2024-2025 Nand Compute LLC | All Rights Reserved 
#
####################################################################

import os
import re

# System file locations
CMDLINE_FILE = '/boot/firmware/cmdline.txt'
MAXFREQ_FILE = '/sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_max_freq'
MODEL_FILE   = '/sys/firmware/devicetree/base/model'
OS_FILE      = '/etc/os-release'

def get_pi_config():
    '''Query system files to get current configuration.'''
    config = dict()
    config['rpi_model'] = find_rpi_model()
    config['os_version'] = find_os_version()
    config['cpu_arch'] = find_cpu_arch()
    config['max_cpu_num'] = find_max_cpus()
    config['max_cpu_freq'] = find_max_cpu_freq()
    return config

def find_cpu_arch():
    '''Find CPU Architecture (i.e. aarch64).'''
    return os.uname().machine

def find_max_cpu_freq():
    '''Find Max CPU Frequency and return in MHz.'''
    with open(MAXFREQ_FILE, 'r') as f:
        output = f.read()
    max_cpu_freq = int(output) / 1000
    return max_cpu_freq

def find_max_cpus():
    '''Find the number of available CPU Cores.'''
    # Open cmdline.txt and read all the contents
    with open(CMDLINE_FILE, 'r') as f:
        output = f.read()

    # Look for maxcpus string
    x = re.findall('maxcpus=\d+', output)
    if len(x) < 1:
        return -1
    
    # Extract max cpu setting and convert to int
    max_cpus = x[0].replace('maxcpus=', '')
    max_cpus = int(max_cpus)
    return max_cpus

def find_os_version():
    '''Find the version of the Operating System.'''
    with open(OS_FILE, 'r') as f:
        output = f.read()
    
    # Look for OS version string
    x = re.findall('PRETTY_NAME="(.+)"', output)
    if len(x) < 1:
        return ''
    
    # Extract OS version from PRETTY_NAME string
    os_version = x[0].replace('PRETTY_NAME=', '')
    os_version = os_version.replace('"', '')
    return os_version

def find_rpi_model():
    '''Find the Raspberry Pi board model.'''
    with open(MODEL_FILE, 'r') as f:
        output = f.read()
    # Remove NULL characeter
    rpi_model = output.replace('\x00', '')
    return rpi_model

