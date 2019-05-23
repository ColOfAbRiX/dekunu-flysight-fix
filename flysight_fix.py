#!/usr/bin/env python3

#
#  Copyright 2019 Fabrizio Colonna <colofabrix@tin.it>
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

#
# Requirements:
#   Python 3
#   Numpy and Pandas python libraries
#

#
# Flysight format - http://flysight.ca/wiki/index.php/File_format
#
#   Column  Content
#   time    Time in ISO8601 format
#   lat     Latitude (degrees)
#   lon     Longitude (degrees)
#   hMSL    Height above sea level (m)
#   velN    Velocity north (m/s)
#   velE    Velocity east (m/s)
#   velD    Velocity down (m/s)
#   hAcc    Horizontal accuracy (m)
#   vAcc    Vertical accuracy (m)
#   sAcc    Speed accuracy (m/s)
#   gpsFix  GPS fix type (3 = 3D)
#   numSV   Number of satellites used in fix
#

from argparse import ArgumentParser
import pandas as pd
import numpy as np
import os

# Interpret command line
parser = ArgumentParser()
parser.add_argument(
    'dekunu_input_csv',
    help="The raw Dekunu CSV file"
)
parser.add_argument(
    '--smooth',
    type=int,
    help="If specified will average the data over specified time points"
)
args = parser.parse_args()

# Load CSV file
with open(args.dekunu_input_csv) as csv_file:
    df = pd.read_csv(csv_file)

# Adjust various things in formatting
df = df.iloc[1:]
df['datetime'] = pd.to_datetime(df['time'])
df = df.set_index('time')
df['velD'] = df['velD'].astype(np.float64)

# Calculate speed
shifted_1 = df.shift(1)
time_deltas = (df['datetime'] - shifted_1['datetime']) / np.timedelta64(1, 's')
df['velD'] = -(df['hMSL'] - shifted_1['hMSL']) / time_deltas

# Smooth data
if args.smooth is not None or args.smooth > 1:
    for col in ['velN', 'velE', 'velD']:
        df[col] = df[col].rolling(window=args.smooth).mean()
    df = df.iloc[args.smooth:]

df = df.drop("datetime", axis=1)
print(df.head())

# Save CSV file
file_name, file_ext = os.path.splitext(args.dekunu_input_csv)
with open("%s_fixed%s" % (file_name, file_ext), 'w') as csv_file:
    df.to_csv(csv_file)
