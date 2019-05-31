#!/usr/bin/env python

##
## @file    printModelParameters.py
## @brief   Prints parameters and species (and their values) in a given SBML Document
## @author  Jean-Marie
##
##
## <!--------------------------------------------------------------------------
## JMB LICENSE TERMS: TO BE CHANGED
## This sample program is distributed under a different license than the rest
## of libSBML.  This program uses the open-source MIT license, as follows:
##
## Copyright (c) 2013-2014 by the University of Southern California
## (California, USA).  All rights reserved.
##
## Permission is hereby granted, free of charge, to any person obtaining a
## copy of this software and associated documentation files (the "Software"),
## to deal in the Software without restriction, including without limitation
## the rights to use, copy, modify, merge, publish, distribute, sublicense,
## and/or sell copies of the Software, and to permit persons to whom the
## Software is furnished to do so, subject to the following conditions:
##
## The above copyright notice and this permission notice shall be included in
## all copies or substantial portions of the Software.
##
## THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
## IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
## FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
## THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
## LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
## FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
## DEALINGS IN THE SOFTWARE.
##
## Neither the name of USC, nor the names of any contributors, may be used to endorse
## or promote products derived from this software without specific prior
## written permission.
## ------------------------------------------------------------------------ -->
##


import sys
import os.path
from libsbml import *
from roadrunner import *

## Prints the model parameters
#@param filename of the model (.xml included)
def printModelParameters (filename):
    r=roadrunner.RoadRunner(filename)
    #r.selections = ['time'] + resSelected

    # ====================================================================================
    # CHANGE PARAM VALUES ACCORDING TO USER PREFS
    # ====================================================================================

    print '=== Model contains ', r.model.keys().__len__() , 'parameters and species. ==='

    #print r.model.keys()
    #for i in range (1, len(r.model.key(), 1)):
    for i in range (1, r.model.keys().__len__(), 1):
        print r.model.items()[i]
    #print r.model.items()


def printModelBoundarySpecies (filename):
    r=roadrunner.RoadRunner(filename)

    print '=== Model contains ', r.model.getNumBoundarySpecies() , 'boundary species. ==='

    for i in range (0, r.model.getNumBoundarySpecies(), 1):
        print r.model.getBoundarySpeciesIds()[i]
    #print r.model.items()


def printModelCompartment (filename):
    r=roadrunner.RoadRunner(filename)

    print '=== Model contains ', r.model.getNumCompartments() , 'compartment. ==='

    for i in range (0, r.model.getNumCompartments(), 1):
        print r.model.getCompartmentIds()[i]



#getNumGlobalParameters

def main (args):
    """Usage: printModelParameters filename
    """
    if (len(args) != 2):
        print("\n" + "Usage: printModelParameters filename" + "\n" + "\n");
        return 1;

    filename = args[1];
    document = readSBML(filename);

    if (document.getNumErrors() > 0):
        print("Encountered the following SBML errors:" + "\n");
        document.printErrors();
        return 1;

    model = document.getModel();

    if (model == None):
        print("No model present." + "\n");
        return 1;

    print 'COMPARTMENT'
    printModelCompartment (filename);
    print;

    print 'GLOBAL PARAMETERS AND SPECIES'
    printModelParameters(filename);
    print;

    print 'BOUNDARY SPECIES'
    printModelBoundarySpecies (filename);

    return 0;

if __name__ == '__main__':
    main(sys.argv)