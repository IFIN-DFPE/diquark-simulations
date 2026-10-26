#!/usr/bin/env bash
#SBATCH --job-name=pythia_generate_minbias
#SBATCH --output=pythia_generate_minbias.log
#SBATCH --error=pythia_generate_minbias.err
#SBATCH --time=24:00:00
#SBATCH --partition=cpu-wide

module add tools/hep/pythia
module add libraries/hep/hepmc/2

./main.exe ./MinBias_PileUp.pythia8.cmnd MinBias.hepmc &> pythia.log

chmod a-w MinBias.hepmc

module add tools/hep/delphes
hepmc2pileup MinBias.pileup MinBias.hepmc
