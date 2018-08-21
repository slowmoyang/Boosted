from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import ROOT
from ROOT import gROOT
from ROOT import gSystem
from ROOT import gInterpreter

from utils import load_fastjet
from utils import load_delphes
load_fastjet()
load_delphes()

from ROOT import fastjet


class EasyJet(object):
    def __init__(self,
                 algorithm="antikt_algorithm",
                 radius=0.4):

        gROOT.ProcessLine("std::vector<fastjet::PseudoJet> particles;")
        gROOT.ProcessLine("fastjet::JetDefinition definition(fastjet::{algorithm}, {radius})".format(
            algorithm=algorithm,
            radius=radius))
        gROOT.ProcessLine("fastjet::ClusterSequence cluster_seq(particles, definition)")

        self._particles = getattr(ROOT, "particles")
        self._definition = getattr(ROOT, "definition")
        self._cluster_seq = getattr(ROOT, "cluster_seq")

        self._algorithm = algorithm
        self._radius = radius

    @property
    def algorithm(self):
        return self._algorithm

    @algorithm.setter
    def algorithm(self, algorithm_):
        self._algoritmh = algorithm_ 
        self._reassign_definition()
        self._reassign_cluster_seq()

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, radius_):
        self._radius = radius_ 
        self._reassign_definition()
        self._reassign_cluster_seq()

    def _reassign_definition(self): 
        gROOT.ProcessLine("definition = fastjet::JetDefinition(fastjet::{algorithm}, {radius})".format(
            algorithm=self._algorithm,
            radius=self._radius))

    def _reassign_cluster_seq(self):
        gROOT.ProcessLine("cluster_seq = fastjet::ClusterSequence(particles, definition)")

    def __str__(self):
        return self._definition.description()

    def cluster_from_tree(self, tree, entry=None):
        if entry is not None:
            tree.GetEntry(entry)

        self._particles.clear()
        for eflow_obj in [tree.EFlowTrack, tree.EFlowPhoton, tree.EFlowNeutralHadron]:
            for each in eflow_obj:
                p4 = each.P4()
                particle = fastjet.PseudoJet(p4.X(), p4.Y(), p4.Z(), p4.E())
                self._particles.push_back(particle)
        self._reassign_cluster_seq()
        jets = fastjet.sorted_by_pt(self._cluster_seq.inclusive_jets())
        return jets

    def cluster_from_jet(self, jet):
        """cluster jets from constituents from a 'Jet' instance
        Args:
          jet: An instance of 'Jet'
        """
        self._particles.clear()

        for each in jet.Constituents:
            p4 = each.P4()
            particle = fastjet.PseudoJet(p4.X(), p4.Y(), p4.Z(), p4.E())
            self._particles.push_back(particle)
        self._reassign_cluster_seq()
        jets = fastjet.sorted_by_pt(self._cluster_seq.inclusive_jets())
        return jets

    # TODO remove all trace like so file and include path when call __del__
    # or use global variable to count and indicate # of instance of EasyJet,
    # and then use the suffix of variable name like particles_<index>
