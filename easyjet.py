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


_INSTANCE_COUNT = 0


class EasyJet(object):
    def __init__(self,
                 algorithm="antikt_algorithm",
                 radius=0.4):
        global _INSTANCE_COUNT
        _INSTANCE_COUNT += 1
        self._instance_count = _INSTANCE_COUNT

        self._particles_name = "particles_{:d}".format(self._instance_count)
        self._definition_name = "definition_{:d}".format(self._instance_count)
        self._cluster_seq_name = "cluster_seq_{:d}".format(self._instance_count)

        gROOT.ProcessLine("std::vector<fastjet::PseudoJet> {name};".format(
            name=self._particles_name))
        gROOT.ProcessLine("fastjet::JetDefinition {name}(fastjet::{algorithm}, {radius});".format(
            name=self._definition_name,
            algorithm=algorithm,
            radius=radius))
        gROOT.ProcessLine("fastjet::ClusterSequence {cluster_seq_name}({particles_name}, {definition_name})".format(
            cluster_seq_name=self._cluster_seq_name,
            particles_name=self._particles_name,
            definition_name=self._definition_name))

        self._particles = getattr(ROOT, self._particles_name)
        self._definition = getattr(ROOT, self._definition_name)
        self._cluster_seq = getattr(ROOT, self._cluster_seq_name)

        self._algorithm = algorithm
        self._radius = radius

    @property
    def algorithm(self):
        return self._algorithm

    @algorithm.setter
    def algorithm(self, algorithm_):
        self._algoritmh = algorithm_ 
        self._assign_definition()
        self._assign_cluster_seq()

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, radius_):
        self._radius = radius_ 
        self._assign_definition()
        self._assign_cluster_seq()

    def _assign_definition(self): 
        gROOT.ProcessLine("{name} = fastjet::JetDefinition(fastjet::{algorithm}, {radius})".format(
            name=self._definition_name,
            algorithm=self._algorithm,
            radius=self._radius))

    def _assign_cluster_seq(self):
        gROOT.ProcessLine("{cluster_seq_name} = fastjet::ClusterSequence({particles_name}, {definition_name})".format(
            cluster_seq_name=self._cluster_seq_name,
            particles_name=self._particles_name,
            definition_name=self._definition_name))

    def __str__(self):
        return self._definition.description() + " (Instance count: {:d})".format(self._instance_count)

    def cluster_from_tree(self, tree, entry=None):
        if entry is not None:
            tree.GetEntry(entry)

        self._particles.clear()
        for eflow_obj in [tree.EFlowTrack, tree.EFlowPhoton, tree.EFlowNeutralHadron]:
            for each in eflow_obj:
                p4 = each.P4()
                particle = fastjet.PseudoJet(p4.X(), p4.Y(), p4.Z(), p4.E())
                self._particles.push_back(particle)
        self._assign_cluster_seq()
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
        self._assign_cluster_seq()
        jets = fastjet.sorted_by_pt(self._cluster_seq.inclusive_jets())
        return jets

    # TODO remove all trace like so file and include path when call __del__
    # or use global variable to count and indicate # of instance of EasyJet,
    # and then use the suffix of variable name like particles_<index>
