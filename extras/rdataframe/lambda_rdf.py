#!/usr/bin/env python3
"""Lambda -> p pi- with ROOT RDataFrame (PyROOT).

Same physics as the stand-alone uproot example, expressed in ROOT's columnar
RDataFrame. A small JIT-compiled C++ helper builds the per-event proton x pi-
invariant masses; RDataFrame histograms them in one declarative pass.

Environment: ROOT (e.g. inside eic-shell / Key4hep). Run with any EDM4eic
reconstruction file, read in place over root:// (discover one as in Episode 3):
    eic-shell -- python3 lambda_rdf.py root://dtn-eic.jlab.org//volatile/eic/EPIC/RECO/<campaign>/.../file.root

Output: lambda_rdf.pdf  (and the peak bin centre printed to stdout, ~1.1157 GeV).
"""
import sys
import ROOT

ROOT.gInterpreter.Declare(r'''
#include "ROOT/RVec.hxx"
#include <cmath>
using namespace ROOT::VecOps;

// invariant mass of every proton x pi- pair in one event
RVec<double> lambda_mass(const RVec<int>& pdg,
                         const RVec<float>& px,
                         const RVec<float>& py,
                         const RVec<float>& pz) {
    const double MP = 0.9382720813, MPI = 0.13957061;
    RVec<double> out;
    auto ip = Nonzero(pdg ==  2212);   // protons
    auto ii = Nonzero(pdg ==  -211);   // pi-
    for (auto a : ip) {
        double Ep = std::sqrt(px[a]*px[a] + py[a]*py[a] + pz[a]*pz[a] + MP*MP);
        for (auto b : ii) {
            double Epi = std::sqrt(px[b]*px[b] + py[b]*py[b] + pz[b]*pz[b] + MPI*MPI);
            double E = Ep + Epi, X = px[a]+px[b], Y = py[a]+py[b], Z = pz[a]+pz[b];
            out.push_back(std::sqrt(std::max(E*E - (X*X + Y*Y + Z*Z), 0.0)));
        }
    }
    return out;
}
''')


def main(path):
    df = ROOT.RDataFrame("events", path)
    df = df.Define("m_lambda",
                   "lambda_mass(ReconstructedChargedParticles.PDG,"
                   "ReconstructedChargedParticles.momentum.x,"
                   "ReconstructedChargedParticles.momentum.y,"
                   "ReconstructedChargedParticles.momentum.z)")
    h = df.Histo1D(("h", "#Lambda#rightarrow p#pi^{-};m(p,#pi) [GeV];pairs",
                    200, 1.05, 1.25), "m_lambda")
    c = ROOT.TCanvas("c", "c", 800, 600)
    h.Draw("HIST E")
    c.SaveAs("lambda_rdf.pdf")
    print(f"entries={h.GetEntries():.0f}  "
          f"peak bin centre={h.GetBinCenter(h.GetMaximumBin()):.4f} GeV")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("usage: lambda_rdf.py <EDM4eic .root file (local path or root:// URL)>")
    main(sys.argv[1])
