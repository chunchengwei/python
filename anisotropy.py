#!/home/weicc/.pyenv/shims/python
# encoding: utf-8
#******************************************************************************
# File Name: anisotropy.py
# Author: Chuncheng Wei
# Mail: weicc1989@gmail.com
# Created Time : Wed 25 Oct 2017 10:55:11 PM CST
# Last Modified: Mon 27 Nov 2017 02:23:13 PM CST
#******************************************************************************

import pyfits, numpy, math
from numpy import savetxt

# constant
C = 2.99792458e10
kpc = 3.08568e21
m_electron = 0.511

D0_xx = 5.8e28
D_rigid_br = 4.0e3
D_g = 0.33

# function
# lnln interp
def lnln_interp(ene, flux, eout):
    fout = numpy.zeros(len(eout), dtype='float')
    up = 0
    for (i,en) in enumerate(eout):

        # find up index
        if (en <= ene[0]):
            up = 1
        elif (en >= ene[-1]):
            up = len(ene)-1
        else:
            while (en > ene[up]):
                up += 1

        # interp
        if (ene[up] and ene[up-1] and flux[up] and flux[up-1]):
            sl =  math.log(flux[up]/flux[up-1]) / math.log(ene[up]/ene[up-1])
            fout[i] = flux[up-1] * (en/ene[up-1]) ** sl
        else:
            fout[i] = 0

    return fout

# solar modu for electron and positron
def solar_modu(ene, flux, phi):
    etemp = ene + phi
    ftemp = lnln_interp(ene, flux, etemp)
    fout = ftemp * ene * (ene+2*m_electron) / (etemp*(etemp+2* m_electron))
    return fout


# read fits
#  hdu  = pyfits.open("galp54nuclei_full_54_convACE.gz")
hdu  = pyfits.open("galp54nuclei_full_54_PBCMED.gz")
hdr  = hdu[0].header
data = hdu[0].data

rmin = hdr['CRVAL1']
dr   = hdr['CDELT1']
nr   = hdr['NAXIS1']

zmin = hdr['CRVAL2']
dz   = hdr['CDELT2']
nz   = hdr['NAXIS2']

emin = hdr['CRVAL3']
de   = hdr['CDELT3']
ne   = hdr['NAXIS3']

# set grid
R = numpy.arange(nr) * dr + rmin
Z = numpy.arange(nz) * dz + zmin
Ekin = 10 ** (numpy.arange(ne) * de + emin)

Etot     = Ekin + m_electron
P        = numpy.sqrt(Etot ** 2 - m_electron ** 2)
gamma    = Etot / m_electron
beta     = P / Etot
rigidity = P

# Dxx
Dxx = beta * D0_xx * (rigidity/D_rigid_br) ** D_g
#  Dxx = D0_xx * (Ekin/D_rigid_br) ** D_g



# find sun id
iz=(int)(1.e-6 - zmin/ dz)
ir=(int)(8.5 - rmin/ dr)
w1=(R[ir+1]-8.5)/dr
w2=(8.5-R[ir])/dr


# particle
# shape => [E, Z, R]
sec_positron = data[0]
sec_electron = data[1]
pri_electron = data[2]
sum_e = sec_positron + sec_electron + pri_electron

# solar modu
F00 = sum_e[:,iz  ,ir  ] / Ekin ** 2
F01 = sum_e[:,iz  ,ir+1] / Ekin ** 2
F10 = sum_e[:,iz+1,ir  ] / Ekin ** 2
F11 = sum_e[:,iz+1,ir+1] / Ekin ** 2

F  = F00*w1 + F01*w2
Fz = F10*w1 + F11*w2

modu_F   = solar_modu(Ekin, F,   550)
modu_Fz  = solar_modu(Ekin, Fz,  550)
modu_F00 = solar_modu(Ekin, F00, 550)
modu_F01 = solar_modu(Ekin, F01, 550)

# anisotropy
dFdr = (modu_F00 - modu_F01) / dr
dFdz = (modu_Fz  - modu_F  ) / dz
gradF = numpy.sqrt(dFdr ** 2 + dFdz **2)

anisotropy = 3 * Dxx / C / kpc * gradF / modu_F

Ekin *= 1e-3

# save
savetxt("aniso", numpy.vstack((Ekin, anisotropy)).transpose(), delimiter='\t')
