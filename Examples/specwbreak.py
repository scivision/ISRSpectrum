#!/usr/bin/env python
"""
Created on Sat Aug 27 22:05:42 2016

@author: John Swoboda
"""
import numpy as np
from matplotlib.pyplot import subplots,show
import seaborn as sns
sns.set_style("white")
sns.set_context("talk",font_scale=1.25)
#
from ISRSpectrum.ISRSpectrum import ISRSpectrum


if __name__== '__main__':

    databloc = np.array([[1e11,1e3],[1e11,2.5e3]])
    f = np.linspace(3.03e6,3.034e6,256)
    f_n=-f[::-1]
#    f = np.logspace(1,np.log10(8e3),2**10)
    ISpec = ISRSpectrum(centerFrequency = 449e6,f=f,dFlag=True)
    ISpec_n = ISRSpectrum(centerFrequency = 449e6,f=f_n,dFlag=True)
    ISpec_ion = ISRSpectrum(centerFrequency = 449e6, nspec=256, sampfreq=50e3,dFlag=True)
    species=['O+','e-']
#    databloc = np.array([[1.66e10,863.],[1.66e10,863.]])

    flims=np.array([3.03e6,3.034e6])
    #%% With B-Field
    eline = ISpec.getspecsep(databloc,species)[1]
    eline_neg = ISpec_n.getspecsep(databloc,species)[1]
    fion,ionline= ISpec_ion.getspecsep(databloc,species)

    fall=np.concatenate((f_n,fion,f),0)
    specall=np.concatenate((eline_neg/eline_neg.max(),ionline/ionline.max(),eline/eline.max()),0)


    fig,(ax,ax2,ax3) = subplots(1,3,sharey=True, figsize=(10,3.5),facecolor='w')


    l1=ax.plot(fall*1e-3,specall,'-',lw=3)[0]
    l1=ax2.plot(fall*1e-3,specall,'-',lw=3)[0]
    l1=ax3.plot(fall*1e-3,specall,'-',lw=3)[0]
    sns.despine()
    ax.set_xlim(f_n.min()*1e-3,f_n.max()*1e-3)
    ax2.set_xlim(fion.min()*1e-3,fion.max()*1e-3)
    ax3.set_xlim(f.min()*1e-3,f.max()*1e-3)

    ax.spines['right'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['left'].set_visible(False)
    ax3.spines['left'].set_visible(False)
    d=.015
    kwargs = dict(transform=ax.transAxes, color='k', clip_on=False)
    ax.plot((1-d,1+d), (-d,+d), **kwargs)
    kwargs.update(transform=ax2.transAxes)  # switch to the bottom axes
    ax2.plot((-d,+d), (-d,+d), **kwargs)
    ax2.plot((1-d,1+d), (-d,+d), **kwargs)

    kwargs.update(transform=ax3.transAxes)  # switch to the bottom axes
    ax3.plot((-d,+d), (-d,+d), **kwargs)

    ax.xaxis.set_ticks(-flims*1e-3)
    ax3.xaxis.set_ticks(flims*1e-3)
    ax2.set_xlabel('Frequency (kHz)')
    ax.set_title('Plasma Line')
    ax2.set_title('Ion Line')
    ax3.set_title('Plasma Line')
    ax.set_ylabel('Normalized Amplitude')

    fig.suptitle('ISR Spectrum')

    fig.tight_layout()
    fig.subplots_adjust(top=0.82)

    fig.savefig('Specwbreaks.eps',bbox_inches='tight')

    show()