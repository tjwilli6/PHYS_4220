"""
Class to animate results of the three-body problem

Usage:
import animate3B
...

x1,x2,x3,y1,y2,y3 = three_body_function(*args)

animation = ThreeBodyAnimation(x1,x2,x3,y1,y2,y3,mass)
animation.run("filename.mp4",speed=15)

0 < speed < 20
"""


import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation


class ThreeBodyAnimation:
    def __init__(self,x1,x2,x3,y1,y2,y3,mass=[],cmframe=True,figsize=(8,5)):
        self.__x = [np.array(ix) for ix in [x1,x2,x3]]
        self.__y = [np.array(iy) for iy in [y1,y2,y3]]
        self.__mass = np.array(mass)
        self.cmframe = cmframe
        self.figsize = figsize
        self.__setup__()

        
    def __setup__(self):
        self.__transform_frame__()
        self.__setup_plots__()
        
    def __get_scatter_size__(self):
        sizemin = 10
        if self.__mass.size:
            mmass = np.array(self.__mass) / self.__mass.sum()
            size = 500 * mmass
            size[size <sizemin] = sizemin
        else:
            size = [sizemin,sizemin,sizemin]
        return size
    
    def __transform_frame__(self):
        if self.cmframe:
            xCM = (self.__x[0] * self.__mass[0] + self.__x[1] * self.__mass[1] + 
                   self.__x[2] * self.__mass[2]) / sum(self.__mass)
            yCM = (self.__y[0] * self.__mass[0] + self.__y[1] * self.__mass[1] + 
                   self.__y[2] * self.__mass[2]) / sum(self.__mass)
            for i in range(len(self.__x)):
                self.__x[i] = self.__x[i] - xCM
                self.__y[i] = self.__y[i] - yCM
    
    def __setup_plots__(self):
        self.__fig = plt.figure(figsize=self.figsize)
        ax1 = plt.gca()
        self.__ax1 = ax1
        size = self.__get_scatter_size__()
        orbit1, = ax1.plot( [],[],ls='--',c='blue' )
        marker1 = ax1.scatter([],[],c='blue',s=size[0],zorder=5)
        orbit2, = ax1.plot( [],[],ls='--',c='green')
        marker2 = ax1.scatter([],[],c='green',s=size[1],zorder=6)
        orbit3, = ax1.plot( [],[],ls='--',c='red' )
        marker3 = ax1.scatter([],[],c='red',s=size[2],zorder=7)
        x0 = [self.__x[i][0] for i in range(3)]
        y0 = [self.__y[i][0] for i in range(3)]
        ax1.set_xlim(min(x0)-1,max(x0)+1)
        ax1.set_ylim(min(y0)-1,max(y0)+1)
        ax1.set_aspect('equal')
        self.__orbit1 = orbit1
        self.__orbit2 = orbit2
        self.__orbit3 = orbit3
        self.__marker1 = marker1
        self.__marker2 = marker2
        self.__marker3 = marker3
        
    def __anim__init__(self):
        self.__orbit1.set_data([], [])
        self.__marker1.set_offsets( np.array( [[],[]]).T )
        self.__orbit2.set_data([], [])
        self.__marker2.set_offsets( np.array( [[],[]]).T )
        self.__orbit3.set_data([], [])
        self.__marker3.set_offsets( np.array( [[],[]]).T )
        return (self.__orbit1,self.__orbit2,self.__orbit3,self.__marker1,self.__marker2,self.__marker3)
    
    def __anim_frame__(self,i):
        self.__orbit1.set_data(self.__x[0][:i],self.__y[0][:i])
        self.__marker1.set_offsets(np.array([ [self.__x[0][i]],[self.__y[0][i]] ]).T )
        self.__orbit2.set_data(self.__x[1][:i],self.__y[1][:i])
        self.__marker2.set_offsets(np.array([ [self.__x[1][i]],[self.__y[1][i]] ]).T )
        self.__orbit3.set_data(self.__x[2][:i],self.__y[2][:i])
        self.__marker3.set_offsets(np.array([ [self.__x[2][i]],[self.__y[2][i]] ]).T )

        if i:
            xmax = max(
                [
                    max(self.__x[0][:i]),
                    max(self.__x[1][:i]),
                    max(self.__x[2][:i])
                ]
            )

            xmin = min(
                [
                    min(self.__x[0][:i]),
                    min(self.__x[1][:i]),
                    min(self.__x[2][:i])
                ]
            )

            ymax = max(
                [
                    max(self.__y[0][:i]),
                    max(self.__y[1][:i]),
                    max(self.__y[2][:i])
                ]
            )

            ymin = min(
                [
                    min(self.__y[0][:i]),
                    min(self.__y[1][:i]),
                    min(self.__y[2][:i])
                ]
            )

            self.__ax1.set_xlim(1.1 * xmin, 1.1 * xmax)
            self.__ax1.set_ylim(1.1 * ymin, 1.1 * ymax)
        return (self.__orbit1,self.__orbit2,self.__orbit3,self.__marker1,self.__marker2,self.__marker3) 
    
    def run(self,fname="animation.mp4",speed=10):
        interval = 21 - speed
        if interval <= 0:
            print("speed parameter must be between 1 and 20")
            return
        anim = FuncAnimation(self.__fig, self.__anim_frame__, init_func=self.__anim__init__,
                               frames=self.__x[0].size, interval=interval, blit=True)

        anim.save(fname)