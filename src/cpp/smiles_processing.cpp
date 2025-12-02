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
    // Define a scaffold SMILES (example: benzene ring)
    // Replace this with your actual scaffold
    std::string scaffoldSmiles = "c1ccccc1";

    // Parse the scaffold
    RWMol* scaffold = SmilesToMol(scaffoldSmiles);
    if (!scaffold) {
        std::cerr << "Failed to parse scaffold SMILES" << std::endl;
        return 1;
    }

    // Generate 2D coordinates for the scaffold
    RDDepict::compute2DCoords(*scaffold);

    std::cout << "Computed 2D coordinates for the SMILES: c1ccccc1." << std::endl;

    delete scaffold;

    std::cout << "Sample finished!" << std::endl;
    return 0;
}
