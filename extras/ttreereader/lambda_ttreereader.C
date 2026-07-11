// lambda_ttreereader.C  —  Lambda -> p pi- with ROOT's TTreeReader.
//
// The classic ROOT event loop, modelled on the ePIC beginner macros. For each
// event it reads the reconstructed-charged-particle PDG codes and momenta, then
// pairs every proton (PDG 2212) with every pi- (PDG -211) and histograms the
// invariant mass. Same physics, same ~1.1157 GeV peak as the uproot / RDataFrame
// examples.
//
// Environment: ROOT (e.g. inside eic-shell / Key4hep). Run with any EDM4eic
// reconstruction file, read in place over root:// (discover one as in Episode 3):
//   eic-shell -- root -l -b -q 'lambda_ttreereader.C("root://epicxrd1.sdcc.bnl.gov:1095//eic/EPIC/RECO/<campaign>/.../file.root")'
//
// Output: lambda_ttreereader.pdf, plus the peak bin centre printed to stdout.
//
// NOTE: the reconstructed momentum branches are stored as `float`, so the
// TTreeReaderArray template parameter must be <float> (not <double>).

#include <TFile.h>
#include <TTreeReader.h>
#include <TTreeReaderArray.h>
#include <TH1F.h>
#include <TCanvas.h>
#include <cmath>
#include <cstdio>

static const double MP = 0.9382720813;   // proton mass (GeV)
static const double MPI = 0.13957061;    // pi mass (GeV)

static double inv_mass(double e1, double x1, double y1, double z1,
                       double e2, double x2, double y2, double z2) {
    double E = e1 + e2, X = x1 + x2, Y = y1 + y2, Z = z1 + z2;
    return std::sqrt(std::max(E*E - (X*X + Y*Y + Z*Z), 0.0));
}

void lambda_ttreereader(const char* file_path = "") {
    if (!file_path || !*file_path) {
        printf("usage: root -l -b -q 'lambda_ttreereader.C(\"<EDM4eic .root file or root:// URL>\")'\n");
        return;
    }
    TFile* f = TFile::Open(file_path);
    if (!f || f->IsZombie()) { printf("cannot open %s\n", file_path); return; }

    TTreeReader reader("events", f);
    TTreeReaderArray<int>   pdg(reader, "ReconstructedChargedParticles.PDG");
    TTreeReaderArray<float> px (reader, "ReconstructedChargedParticles.momentum.x");
    TTreeReaderArray<float> py (reader, "ReconstructedChargedParticles.momentum.y");
    TTreeReaderArray<float> pz (reader, "ReconstructedChargedParticles.momentum.z");

    TH1F* h = new TH1F("h", "#Lambda#rightarrow p#pi^{-};m(p,#pi) [GeV];pairs",
                       200, 1.05, 1.25);

    while (reader.Next()) {
        for (size_t i = 0; i < pdg.GetSize(); ++i) {
            if (pdg[i] != 2212) continue;                 // proton
            double Ep = std::sqrt(px[i]*px[i] + py[i]*py[i] + pz[i]*pz[i] + MP*MP);
            for (size_t j = 0; j < pdg.GetSize(); ++j) {
                if (pdg[j] != -211) continue;             // pi-
                double Epi = std::sqrt(px[j]*px[j] + py[j]*py[j] + pz[j]*pz[j] + MPI*MPI);
                h->Fill(inv_mass(Ep, px[i], py[i], pz[i],
                                 Epi, px[j], py[j], pz[j]));
            }
        }
    }

    TCanvas* c = new TCanvas("c", "c", 800, 600);
    h->Draw("HIST E");
    c->SaveAs("lambda_ttreereader.pdf");
    printf("entries=%.0f  peak bin centre=%.4f GeV\n",
           h->GetEntries(), h->GetBinCenter(h->GetMaximumBin()));
    f->Close();
}
