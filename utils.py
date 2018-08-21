from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import yaml

import ROOT
from ROOT import gInterpreter
from ROOT import gSystem


def get_config(config_path="./config.yaml"):
    with open(config_path, "r") as config_file:
        config = yaml.load(config_file)
    return config  

_CONFIG = get_config()

def load_delphes(delphes_dir=None):
    if hasattr(ROOT, "Delphes"):
        print("'delphes' was already loaded.")
        return None
    if delphes_dir is None:
        delphes_dir = _CONFIG["delphes"]
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
        fastjet_dir = _CONFIG["fastjet"]
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
