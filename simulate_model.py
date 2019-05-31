
import roadrunner, time
from roadrunner import *
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pylab
import os
import sys
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.collections import PolyCollection
from matplotlib.colors import colorConverter


#======================================================================
# SIMULATION PARAMETERS
#======================================================================

model = 'finalModel_NTDiff_and_AMPA.xml'

distance_from_release_site = 0   # to vary from 0 to 0.200 (unit is microm)

# SIMULATION OPTIONS
ptsPerMs = 50    # Nb of points saved per ms. 5 is enough for most simulations. 400 necessary for glutamate concentration profile
simDuration = 60  # Simulation duration
sim_stiffSolver = True  # Simulation solver
sim_varTimeStep = True  # Simulation at var. time step
plotRawResults = True #Plot raw results in subplots (right after simulation)
saveResultsToFile = True #Save results to file

#======================================================================
# SIMULATION
#======================================================================
def simulate(distance):
    loadingTime = time.time()
    ### This is the line that loads the model
    r = RoadRunner(model)
    loadTimeEnd = time.time() - loadingTime
    print 'model loaded with loading time: ' , loadTimeEnd
    # modify the distance
    r.model["distanceAMPA_2"]= distance + 0.001     # Add 1 nm to avoid convergence errors
    print '... for distance = ' , r.model["distanceAMPA_2"] , ' microm'

    # ================== INIT SIMULATOR PARAMETERS OPTIONS ===============
    o = SimulateOptions()
    o.stiff = sim_stiffSolver          # enable still solver
    #o.minimumTimeStep = 1e-2  # internal integrator min time step
    o.maximumTimeStep = 1
    o.absolute = 1e-6
    o.relative = 1e-6
    o.initialTimeStep = 0.001
    o.maximumNumSteps= 10000     # internal integrator max time step (default is 500)
    o.start=0                  # start time
    o.duration= float (simDuration)             # total time step
    o.steps = int (simDuration) * int (ptsPerMs)      # number of points to output
    o.variableStep = sim_varTimeStep

    # record time
    s = time.time()
    # DEFINE RESULTS TO BE STORED/DISPLAYED
    #resSelected = config['Results']['resSelected']
    resSelected = ['V_1', 'NTconcAMPA_2', 'distanceAMPA_2','current_AMPA_3', 'O2_3', 'O3_3', 'O4_3']

    # SPECIFY SIMULATION PARAMETERS
    try:
        r.selections = ['time'] + resSelected
    except RuntimeError:
        print "VARIABLES AVAILABLE:"
        print "==================="
        variousScripts.printModelParameters.printModelParameters(model)
        print "ERROR: One or more results selected does not exist. Double check results selected. ", sys.exc_info()[0]
        exit(0)

    # SIMULATE
    t = r.simulate(o)

    total_time = time.time() - s
    print "\nSimulation lasted ", total_time , 'sec.'


    #PLOTS
    if plotRawResults:
        # Interactive mode ON
        plt.ion()
        f, axarr = plt.subplots(len(resSelected), sharex=True)
        for i in xrange(len(resSelected)):
            axarr[i].plot(t[:,0], t[:,i+1])
            axarr[i].set_title(resSelected[i])
            #axarr[i].plot(t['time'], t[resSelected[i]])
            #axarr[i].set_title(resSelected[i])
        plt.draw()
        # Interactive mode OFF
        plt.ioff()
        #resize and save raw data
        figure = plt.gcf()
        figure.set_size_inches(11,8)
        plt.savefig('rawResults_'+str(distance)+'microm.pdf', dpi=300)

        plt.close()

    #TO SAVE FILE IN TXT (IN ROWS)
    #Save all results
    for i in xrange(len(resSelected)):
        #np.savetxt('test.txt', t[:, 0], t[:, 3])
        #print 'CLEANRESULTS IS ' , str(cleanResults)
        #np.savetxt(resSelected[i]+'_'+str(distance)+'microm.txt',np.vstack( (t[:,0], t[:,i+1]) ).T )
        formatted_dist = "{:0>3d}".format(int(distance*1000))
        np.savetxt(resSelected[i]+'_'+ formatted_dist +'nm.txt',np.vstack( (t[:,0], t[:,i+1]) ).T )

    # Append the list of files to gather all O2, O3 and O4 profiles on 3d graph later on.
    list_of_files_O2.append(('O2_3_'+ formatted_dist +'nm.txt' , 'O2_'+ formatted_dist +'nm'))
    list_of_files_O3.append(('O3_3_'+ formatted_dist +'nm.txt', 'O3_'+ formatted_dist +'nm'))
    list_of_files_O4.append(('O4_3_'+ formatted_dist +'nm.txt', 'O4_'+ formatted_dist +'nm'))

    # At the end, show to ensure window does not close
    #if plotRawResults :
        #plt.show()

# # PLOT ALL PROFILES IN 2D (Not as pretty as 3d)
# def plotResults (datalist, title):
#     for data, label in datalist:
#         pylab.plot( data[:,0], data[:,1], label=label )
#         print "plotting.... " , label
#         pylab.legend()
#         pylab.title(title)
#         pylab.xlabel("Probability")
#         pylab.ylabel("Y Axis Label")
#     # pylab.show()
#     # pylab.savefig(title+'_all_distances.pdf', dpi=300)
#
#     pylab.draw()
#     # Interactive mode OFF
#     pylab.ioff()
#     #resize and save raw data
#     #figure = pylab.gcf()
#     #figure.set_size_inches(11,8)
#     pylab.savefig(title+'_all_distances.pdf', dpi=300)


# PLOT ALL PROFILES IN 3D
def plot3dResults (datalist, title):
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    verts = []
    dist = list()
    currentDistance=0
    for data, label in datalist:
        verts.append(list(zip(data[:,0], data[:,1])))
        dist.append(currentDistance)
        currentDistance = currentDistance + 20

    poly = PolyCollection(verts, facecolors = [cc('r'), cc('g'), cc('b'),
                                           cc('y')])
    poly.set_alpha(0.7)
    ax.add_collection3d(poly, zs=dist, zdir='y')

    ax.set_xlabel('Time (ms)')
    ax.set_xlim3d(0, 60)
    ax.set_ylabel('Distance from release site')
    ax.set_ylim3d(-1, 200)
    ax.set_zlabel('Probability for ' + title)
    ax.set_zlim3d(0, 0.15)

    plt.draw()
    # Interactive mode OFF
    plt.ioff()
    plt.savefig(title+'_all_distances.pdf', dpi=300)
    print "NEW FILE: " + title+'_all_distances.pdf saved to disk'


#================================================================================
#MAIN
#================================================================================
#Create empty list
list_of_files_O2= list()
list_of_files_O3= list()
list_of_files_O4= list()

#initialize color converter
cc = lambda arg: colorConverter.to_rgba(arg, alpha=0.6)

#  LOOP ON THE DISTANCE
for i in range(0, 11):
    # increment distance
    distance_from_release_site = 0.02 * i
    # simulate
    simulate(distance_from_release_site)

# Gather data from the list of files
datalist = [ ( pylab.loadtxt(filename), label ) for filename, label in list_of_files_O2 ]
# ... and plot
plot3dResults(datalist, 'O2')

datalist = [ ( pylab.loadtxt(filename), label ) for filename, label in list_of_files_O3 ]
plot3dResults(datalist, 'O3')

datalist = [ ( pylab.loadtxt(filename), label ) for filename, label in list_of_files_O4 ]
plot3dResults(datalist, 'O4')

print "SIMULATIONS FINISHED. CHECK RESULTS ON CURRENT ACTIVE DIRECTORY"

