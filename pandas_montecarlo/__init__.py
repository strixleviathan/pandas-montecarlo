#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Monte Carlo Simulator
# https://github.com/ranaroussi/pandas-montecarlo
#
# Copyright 2017 Ran Aroussi
#
# Licensed under the GNU Lesser General Public License, v3.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.gnu.org/licenses/lgpl-3.0.en.html
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


__version__ = "0.0.2"
__author__ = "Ran Aroussi"
__all__ = ['montecarlo']

import pandas as pd
import matplotlib.pyplot as plt
from pandas.core.base import PandasObject

def montecarlo(series, sims=100, bust=-1, goal=0):

    if not isinstance(series, pd.Series):
        raise ValueError("Data must be a Pandas Series")

    class __make_object__:
        """Monte Carlo simulation results"""
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)

    def plot(title="Monte Carlo Simulation Results", figsize=None):
        fig, ax = plt.subplots(figsize=figsize)
        ax.plot(compound, lw=1, alpha=.8)
        ax.plot(compound["original"], lw=3, color="r", alpha=.8, label="Original")
        ax.axhline(0, color="black")
        ax.legend()
        ax.set_title(title, fontweight="bold")
        plt.ylabel("Results")
        plt.xlabel("Occurrences")
        plt.show()
        plt.close()

    results = [series.values]
    for i in range(1, sims):
        results.append(series.sample(frac=1).values)

    df = pd.DataFrame(results).T
    df.rename(columns={0:'original'}, inplace=True)

    compound = df.add(1).cumprod()-1
    total = compound
    nav = 100 * compound.add(1)
    dd = nav / nav.cummax() - 1
    nobust = compound[compound.min()[compound.min() > -abs(bust)].index][-1:]


    return __make_object__(**{
        "data": df,
        "stats": {
            "min": round(total.min().values[0],4),
            "max": round(total.max().values[0],4),
            "mean": round(total.mean().values[0],4),
            "median": round(total.median().values[0],4),
            "std": round(total.std().values[0],4),
            "maxdd": round(dd.min().min(),4),
            "bust": len(dd[dd <= -abs(bust)]) / sims,
            "goal": (nobust >= abs(goal)).sum().sum() / sims,
        },
        "maxdd": {
            "max": round(dd.min().min(),4),
            "min": round(dd.max().max(),4),
            "mean": round(dd.mean().mean(),4),
            "median": round(dd.median().median(),4),
            "std": round(dd.std().mean(),4)
        },
        "plot": plot
    })


PandasObject.montecarlo = montecarlo
