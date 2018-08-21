from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import ROOT
from ROOT import gInterpreter
from ROOT import gSystem

_DELPHES_ENV_VAR = "DELPHES"
_FASTJET_ENV_VAR = "FASTJET"

def load_delphes(delphes_dir=None):
    if delphes_dir is None:
        print("Try to find delphes env var")
        delphes_dir = gSystem.Getenv(_DELPHES_ENV_VAR)
        if delphes_dir == "":
            raise OSError
        else:
            print("Found. '{}'".format(delphes_dir))
    else:
        raise OSError

    classes_dir = gSystem.ConcatFileName(delphes_dir, "classes")
    external_dir = gSystem.ConcatFileName(delphes_dir, "external")
    exrootanalysis_dir = gSystem.ConcatFileName(external_dir, "ExRootAnalysis")
    so_file = gSystem.ConcatFileName(delphes_dir, "libDelphes.so")

    gInterpreter.AddIncludePath(delphes_dir)
    gInterpreter.AddIncludePath(classes_dir)
    gInterpreter.AddIncludePath(external_dir)
    gInterpreter.AddIncludePath(exrootanalysis_dir)
    gSystem.Load(so_file)
    gInterpreter.Declare('#include "classes/DelphesClasses.h"')


def load_fastjet(fastjet_dir=None):
    if hasattr(ROOT, "fastjet"):
        print("'fastjet' was already loaded.")
        return None

    if fastjet_dir is None:
        print("Try to find fastjet env var")
        fastjet_dir = gSystem.Getenv(_FASTJET_ENV_VAR)
        if fastjet_dir == "":
            raise OSError
        else:
            print("Found. '{}'".format(fastjet_dir))
    else:
        raise OSError
        
    lib_dir = gSystem.ConcatFileName(fastjet_dir, "lib")
    include_dir = gSystem.ConcatFileName(fastjet_dir, "include")

    libfastjet_so = gSystem.ConcatFileName(lib_dir, "libfastjet.so")
    libfastjettools_so = gSystem.ConcatFileName(lib_dir, "libfastjettools.so")

    gInterpreter.AddIncludePath(include_dir)
    gSystem.Load(libfastjet_so)
    gSystem.Load(libfastjettools_so)
    gInterpreter.Declare('#include "fastjet/PseudoJet.hh"')
    gInterpreter.Declare('#include "fastjet/ClusterSequence.hh"')
    gInterpreter.Declare('#include "fastjet/Selector.hh"')
