import argparse
import pandas as pd

import sys, os

# Disable printing
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore printing
def enablePrint():
    sys.stdout = sys.__stdout__

import warnings
warnings.filterwarnings("ignore")

blockPrint()

parser = argparse.ArgumentParser(description='Get input file and parameters')

parser.add_argument('inputfile', metavar='inputfile', type=str, help='provide input file')

parser.add_argument("--plot", help="use if want to see BJD vs mag plot",
                    action="store_true")

parser.add_argument("--foldedplot", help="use if want to see (BJD mod P) vs mag plot",
                    action="store_true")


args = parser.parse_args()


#print("Input file:")
#print(args.inputfile)

datain=pd.read_csv(args.inputfile,sep=r'\s*',header=0)

from gatspy.periodic import LombScargleFast
dmag=0.000005
nyquist_factor=40

model = LombScargleFast().fit(datain['BJD'], datain['mag'], dmag)
periods, power = model.periodogram_auto(nyquist_factor)

model.optimizer.period_range=(0.2, 10)
period = model.best_period

enablePrint()
print(period)

if args.plot:
    import matplotlib.pyplot as plt
    plt.plot(datain['BJD'],datain['mag'])
    plt.show()

if args.foldedplot:
    import matplotlib.pyplot as plt
    import numpy as np
    BJD=np.asarray(datain['BJD'])
    BJDmodP=np.mod(BJD,period)
    plt.scatter(BJDmodP,datain['mag'])
    plt.show()
