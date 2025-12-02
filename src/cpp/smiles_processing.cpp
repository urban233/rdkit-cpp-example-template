//
//  Copyright (C) 2025 Martin Urban
//

#include <GraphMol/GraphMol.h>
#include <GraphMol/FileParsers/MolSupplier.h>
#include <GraphMol/FileParsers/MolWriters.h>
#include <GraphMol/Depictor/RDDepictor.h>
#include <GraphMol/Substruct/SubstructMatch.h>
#include <iostream>
#include <vector>

using namespace RDKit;

int main() {
    std::string tmp_smiles = "c1ccccc1";
    RWMol* tmp_structure = SmilesToMol(tmp_smiles);
    if (!tmp_structure) {
        std::cerr << "Failed to parse SMILES" << std::endl;
        return 1;
    }
    RDDepict::compute2DCoords(*tmp_structure);

    std::cout << "Computed 2D coordinates for the SMILES: c1ccccc1." << std::endl;

    delete tmp_structure;

    std::cout << "Sample finished!" << std::endl;
    return 0;
}
