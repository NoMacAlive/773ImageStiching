#!/usr/bin/env python

# convolve2D.py - Convolution operations on pixel arrays in 2D
#
# Copyright (C) 2020 Martin Urschler <martin.urschler@auckland.ac.nz>
#
# Original concept by Martin Urschler.
#
# LICENCE (MIT)
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import imageProcessing.utilities as IPUtils
import numpy as np

def computeDerivative(pixel_array, image_width, image_height, kernelAlongX = [], kernelAlongY = []):

    kernelAlongX = np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1 ]])
    kernelAlongY = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1 ]])


    Ix = IPUtils.createInitializedGreyscalePixelArray(image_width, image_height)
    Iy = IPUtils.createInitializedGreyscalePixelArray(image_width, image_height)

    # two pass algorithm for separable convolutions

    kernel_offset = 3//2
    #print("ntap kernel offset", kernel_offset)

    for y in range(image_height):
        for x in range(image_width):
            if x >= kernel_offset and x < image_width - kernel_offset and y >= kernel_offset and y < image_height - kernel_offset :
                convolution = 0.0
                for yy in range(-kernel_offset, kernel_offset+1):
                    for xx in range(-kernel_offset, kernel_offset+1):
                        convolution = convolution + kernelAlongX[kernel_offset+yy,kernel_offset+xx] * pixel_array[y+yy][x+xx]
                Ix[y][x] = convolution

    kernel_offset = 3//2

    for y in range(image_height):
        for x in range(image_width):
            if x >= kernel_offset and x < image_width - kernel_offset and y >= kernel_offset and y < image_height - kernel_offset:
                convolution = 0.0
                for yy in range(-kernel_offset, kernel_offset+1):
                    for xx in range(-kernel_offset, kernel_offset+1):
                        convolution = convolution + kernelAlongY[kernel_offset+yy,kernel_offset+xx] * pixel_array[y+yy][x+xx]
                Iy[y][x] = convolution

    return Ix,Iy


def computeMComponents(Ix,Iy):
    width = len(Ix[0])
    height = len(Ix)
    Ix2 = [[0 for i in range(width)] for j in range(height)]
    Iy2 = [[0 for i in range(width)] for j in range(height)]
    Ixy = [[0 for i in range(width)] for j in range(height)]
    for y in range(height):
        for x in range(width):
            Ix2[y][x] = Ix[y][x]**2
            Iy2[y][x] = Iy[y][x]**2
            Ixy[y][x] = Ix[y][x]*Iy[y][x]
    
    return Ix2,Iy2,Ixy
    