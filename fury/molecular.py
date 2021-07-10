import vtk
from vtk.util import numpy_support


class Molecule(vtk.vtkMolecule):
    """Your molecule class.

    An object that is used to create molecules and store molecular data (e.g.
    coordinate and bonding data).
    This is a more pythonic version of ``vtkMolecule``.
    """


def add_atom(molecule, atomic_num, x_coord, y_coord, z_coord):
    """Add atomic data to our molecule.

    Parameters
    ----------
    molecule : Molecule() object
        The molecule to which the atom is to be added.
    atomic_num : int
        Atomic number of the atom.
    x_coord : float
        x-coordinate of the atom.
    y_coord : float
        y-coordinate of the atom.
    z_coord : float
        z-coordinate of the atom.
    """
    molecule.AppendAtom(atomic_num, x_coord, y_coord, z_coord)


def add_bond(molecule, atom1_index, atom2_index, bond_type=1):
    """Add bonding data to our molecule. Establish a bond of type bond_type
    between the atom at atom1_index and the atom at atom2_index.

    Parameters
    ----------
    molecule : Molecule() object
        The molecule to which the bond is to be added.
    atom1_index : int
        Index of the first atom.
    atom2_index : int
        Index of the second atom.
    bond_type : int (optional)
        Type of bond (single/double/triple). Default: 1
    """
    molecule.AppendBond(atom1_index, atom2_index, bond_type)


def get_total_num_atoms(molecule):
    """Returns the total number of atoms in a given molecule.

    Parameters
    ----------
    molecule : Molecule() object
    """
    return molecule.GetNumberOfAtoms()


def get_total_num_bonds(molecule):
    """Returns the total number of bonds in a given molecule.

    Parameters
    ----------
    molecule : Molecule() object
    """
    return molecule.GetNumberOfBonds()


def get_atomic_number(molecule, atom_index):
    """Get the atomic number of an atom for a specified index.

    Returns the atomic number of the atom present at index atom_index.

    Parameters
    ----------
    molecule : Molecule() object
        The molecule to which the atom belongs.
    atom_index : int
        Index of the atom whose atomic number is to be obtained.
    """
    return molecule.GetAtomAtomicNumber(atom_index)


def set_atomic_number(molecule, atom_index, atomic_num):
    """Set the atomic number of an atom for a specified index.

    Assign atomic_num as the atomic number of the atom present at
    atom_index.

    Parameters
    ----------
    molecule : Molecule() object
        The molecule to which the atom belongs.
    atom_index : int
        Index of the atom to whom the atomic number is to be assigned.
    atom_num : int
        Atomic number to be assigned to the atom.
    """
    molecule.SetAtomAtomicNumber(atom_index, atomic_num)


def get_atomic_position(molecule, atom_index):
    """Get the atomic coordinates of an atom for a specified index.

    Returns the atomic coordinates of the atom present at index atom_index.

    Parameters
    ----------
    molecule : Molecule() object
        The molecule to which the atom belongs.
    atom_index : int
        Index of the atom whose atomic coordinates are to be obtained.
    """
    return molecule.GetAtomPosition(atom_index)


def set_atomic_position(molecule, atom_index, x_coord, y_coord, z_coord):
    """Set the atomic coordinates of an atom for a specified index.

    Assign atom_coordinate to the coordinates of the atom present at
    atom_index.

    Parameters
    ----------
    molecule : Molecule() object
        The molecule to which the atom belongs.
    atom_index : int
        Index of the atom to which the coordinates are to be assigned.
    x_coord : float
        x-coordinate of the atom.
    y_coord : float
        y-coordinate of the atom.
    z_coord : float
        z-coordinate of the atom.
    """
    molecule.SetAtomPosition(atom_index, x_coord, y_coord, z_coord)


def get_bond_type(molecule, bond_index):
    """Get the type of bond for a specified index.

    Returns the type of bond (whether it's a single/double/triple bond)
    present at bond_index.

    Parameters
    ----------
    molecule : Molecule() object
        The molecule to which the bond belongs.
    bond_index : int
        Index of the bond whose type is to be obtained.
    """
    return molecule.GetBondOrder(bond_index)


def set_bond_type(molecule, bond_index, bond_type):
    """Set the bond type of a bond for a specified index.

    Assign bond_type (whether it's a single/double/triple bond) to the bond
    present at the bond_index.

    Parameters
    ----------
    molecule : Molecule() object
        The molecule to which the bond belongs.
    bond_index : int
        Index of the atom to which the coordinates are to be assigned.
    bond_type : int
        Type of the bond (single/double/triple).
    """
    return molecule.SetBondOrder(bond_index, bond_type)


def get_atomic_number_array(molecule):
    """Returns an array of atomic numbers corresponding to the atoms
    present in a given molecule.

    Parameters
    ----------
    molecule : Molecule() object
        The molecule whose atomic number array is to be obtained.
    """
    return numpy_support.vtk_to_numpy(molecule.GetAtomicNumberArray())


def get_bond_types_array(molecule):
    """Returns an array containing the types of the bond (single/double/
    triple) corresponding to the bonds present in the molecule.

    Parameters
    ----------
    molecule : Molecule() object
        The molecule whose bond types array is to be obtained.
    """
    return numpy_support.vtk_to_numpy(molecule.GetBondOrdersArray())


def get_atomic_position_array(molecule):
    """Returns an array of atomic coordinates corresponding to the atoms
    present in the molecule.

    Parameters
    ----------
    molecule : Molecule() object
        The molecule whose atomic position array is to be obtained.
    """
    return numpy_support.vtk_to_numpy(molecule.GetAtomicPositionArray().
                                      GetData())


def deep_copy(molecule1, molecule2):
    """
    Deep copies the atomic information (atoms and bonds) from molecule2 into
    molecule1.

    Parameters
    ----------
    molecule1 : Molecule() object
        The molecule to which the atomic information is copied.
    molecule2 : Molecule() object
        The molecule from which the atomic information is copied.
    """
    molecule1.DeepCopyStructure(molecule2)


def compute_bonding(molecule):
    """
    Uses vtkSimpleBondPerceiver to generate bonding information for a
    molecule.
    vtkSimpleBondPerceiver performs a simple check of all interatomic
    distances and adds a single bond between atoms that are reasonably
    close. If the interatomic distance is less than the sum of the two
    atom's covalent radii plus a tolerance, a single bond is added.

    Parameters
    ----------
    molecule : Molecule() object
        The molecule for which bonding information is to be generated.

    Notes
    -----
    This algorithm does not consider valences, hybridization, aromaticity,
    or anything other than atomic separations. It will not produce anything
    other than single bonds.
    """
    bonder = vtk.vtkSimpleBondPerceiver()
    bonder.SetInputData(molecule)
    bonder.SetTolerance(0.1)
    bonder.Update()
    deep_copy(molecule, bonder.GetOutput())


class MoleculeMapper(vtk.vtkOpenGLMoleculeMapper):
    """Class to create mappers for three types of molecular represenations-
    1. Ball and Stick Representation.
    2. Stick Representation.
    3. Sphere Representation.

    It is used to create mappers which are then used to create actors for the
    above mentioned representations.
    """


def set_molecule_to_mapper(molecule_mapper, molecule):
    """This function performs two tasks -
    1. It sends the molecule data to the mapper object.
    2. It checks if adequate bonding data is available and assigns a bool
    to bonds_data_available accordingly.

    Parameters
    ----------
    molecule_mapper : MoleculeMapper() object
        MoleculeMapper object to which the molecule's atomic info is sent.
    molecule : Molecule object
        Molecule whose atomic info is sent to the mapper.
    """
    molecule_mapper.bonds_data_available = False
    molecule_mapper.SetInputData(molecule)
    if get_bond_types_array(molecule).size == get_total_num_bonds(molecule) \
       and get_total_num_bonds(molecule) > 0:
        molecule_mapper.bonds_data_available = True


def molecule_mapper_render_atoms(molecule_mapper, choice):
    """Set whether or not to render atoms for a given MoleculeMapper object.

    Parameters
    ----------
    molecule_mapper : MoleculeMapper() object
    choice : bool
        * If choice is True, atoms are rendered.
        * If choice is False, atoms are not rendered.
    """
    molecule_mapper.SetRenderAtoms(choice)


def molecule_mapper_render_bonds(molecule_mapper, choice):
    """Set whether or not to render bonds for a given MoleculeMapper object.

    Parameters
    ----------
    molecule_mapper : MoleculeMapper() object
    choice : bool
        * If choice is True, bonds are rendered.
        * If choice is False, bonds are not rendered.
    """
    molecule_mapper.SetRenderBonds(choice)


def set_atomic_radius_type(molecule_mapper, radius_type):
    """Set the type of radius used to generate the atoms for a given
    MoleculeMapper object.

    Parameters
    ----------
    molecule_mapper : MoleculeMapper() object
    radius_type : string
        The type of radius used to generate the atoms. Three valid radius
        types -
        * 'Unit': Use unit radius for all atoms (atomic radius = 1 for all
          atoms, irrespective of element)
        * 'VDW': Use Van Der Waals radius for all atoms
                 (unique to each element)
        * 'Covalent': Use covalent radius for all atoms
                      (unique to each element)
    """
    if radius_type == 'Unit':
        molecule_mapper.SetAtomicRadiusTypeToUnitRadius()
    elif radius_type == 'VDW':
        molecule_mapper.SetAtomicRadiusTypeToVDWRadius()
    elif radius_type == 'Covalent':
        molecule_mapper.SetAtomicRadiusTypeToCovalentRadius()


def set_atomic_radius_scale(molecule_mapper, scale_factor):
    """Set the uniform scaling factor applied to the atoms for a given
    MoleculeMapper object.

    Parameters
    ----------
    molecule_mapper : MoleculeMapper() object
    scale_factor : float
        Scaling factor to be applied to the atoms.
    """
    molecule_mapper.SetAtomicRadiusScaleFactor(scale_factor)


def set_bond_colormode(molecule_mapper, choice):
    """Set the method by which bonds are colored for a a given MoleculeMapper
    object.

    Parameters
    ----------
    molecule_mapper : MoleculeMapper() object
    choice : string
        * If choice is 'discrete', each bond is colored using the same lookup
          table as the atoms at each end, with a sharp color boundary at the
          bond center.
        * If choice is 'single', all bonds will be of same color.
    """
    if choice == 'discrete':
        molecule_mapper.SetBondColorMode(1)
    elif choice == 'single':
        molecule_mapper.SetBondColorMode(0)


def set_atom_colormode(molecule_mapper, choice):
    """Set the method by which atoms are colored for a given MoleculeMapper
    object.

    Parameters
    ----------
    molecule_mapper : MoleculeMapper() object
    choice : string
        * If choice is 'discrete', atoms are colored using CPK coloring
          convention.
        * If choice is 'single', all atoms will be of same color.
    """
    if choice == 'discrete':
        molecule_mapper.SetAtomColorMode(1)
    elif choice == 'single':
        molecule_mapper.SetAtomColorMode(0)


def set_bond_thickness(molecule_mapper, bondThickness):
    """Sets the thickness of the bonds (i.e. thickness of tubes which are used
    to render bonds) for a given MoleculeMapper object.

    Parameters
    ----------
    molecule_mapper : MoleculeMapper() object
    bondThickness: float
        Thickness of the bonds.
    """
    molecule_mapper.SetBondRadius(bondThickness)


def set_multi_bonds(molecule_mapper, choice):
    """Set whether multiple tubes will be used to represent multiple bonds for
    a given MoleculeMapper object.

    Parameters
    ----------
    molecule_mapper : MoleculeMapper() object
    choice : bool
        * If choice is True, multiple bonds (double, triple) will be shown by
          using multiple tubes.
        * If choice is False, all bonds (single, double, triple) will be
          shown as single bonds (i.e. shown using one tube each).
    """
    molecule_mapper.SetUseMultiCylindersForBonds(choice)


def config_mapper_to_molecular_sphere(molecule_mapper, colormode):
    """Configure settings to create a molecular sphere representation for a
    given MoleculeMapper object.

    Parameters
    ----------
    molecule_mapper : MoleculeMapper() object
    colormode : string
        Set the colormode for coloring the atoms. Two valid color modes -
        * 'discrete': Atoms are colored using CPK coloring convention.
        * 'single': All atoms are colored with same color(grey)

        RGB tuple used for coloring the atoms when 'single' colormode is
        selected: (150, 150, 150)
    """
    molecule_mapper_render_atoms(molecule_mapper, True)
    molecule_mapper_render_bonds(molecule_mapper, False)
    set_atomic_radius_type(molecule_mapper, 'VDW')
    set_atomic_radius_scale(molecule_mapper, 1)
    set_atom_colormode(molecule_mapper, colormode)


def config_mapper_to_ball_stick(molecule_mapper, colormode, atom_scale_factor,
                                bond_thickness, multiple_bonds):
    """Configure settings to create a molecular ball and stick representation
    for a given MoleculeMapper object.

    Parameters
    ----------
    molecule_mapper : MoleculeMapper() object
    colormode : string
        Set the colormode for coloring the atoms. Two valid color modes -
        * 'discrete': Atoms and bonds are colored using CPK coloring
          convention.
        * 'single': All atoms are colored with same color(grey) and all
          bonds are colored with same color(dark grey).
        * RGB tuple used for coloring the atoms when 'single' colormode is
        selected: (150, 150, 150)
        * RGB tuple used for coloring the bonds when 'single' colormode is
        selected: (50, 50, 50)

    atom_scale_factor : float
        Scaling factor to be applied to the atoms.
    bond_thickness : float
        Used to manipulate the thickness of bonds (i.e. thickness of tubes
        which are used to render bonds)
    multiple_bonds : string
        Set whether multiple tubes will be used to represent multiple
        bonds. Two valid choices -
        * 'On': multiple bonds (double, triple) will be shown by using
          multiple tubes.
        * 'Off': all bonds (single, double, triple) will be shown as single
          bonds (i.e. shown using one tube each).
    """
    if molecule_mapper.bonds_data_available:
        molecule_mapper_render_atoms(molecule_mapper, True)
        molecule_mapper_render_bonds(molecule_mapper, True)
        set_bond_thickness(molecule_mapper, bond_thickness/10)
        set_atomic_radius_type(molecule_mapper, 'VDW')
        set_atomic_radius_scale(molecule_mapper, atom_scale_factor)
        if multiple_bonds == 'On':
            set_multi_bonds(molecule_mapper, True)
        elif multiple_bonds == 'Off':
            set_multi_bonds(molecule_mapper, False)
    else:
        print("Inadequate Bonding data")

    set_atom_colormode(molecule_mapper, colormode)
    set_bond_colormode(molecule_mapper, colormode)


def config_mapper_to_stick(molecule_mapper, colormode, bond_thickness):
    """Configure settings to create a molecular stick representation for a
    given MoleculeMapper object.

    Parameters
    ----------
    molecule_mapper : MoleculeMapper() object
    colormode : string
        Set the colormode for coloring the bonds. Two valid color modes -
        * 'discrete': Bonds are colored using CPK coloring convention.
        * 'single': All bonds are colored with the same color (dark grey).
        * RGB tuple used for coloring the bonds when 'single' colormode is
          selected: (50, 50, 50)

    atom_scale_factor : float
        Scaling factor to be applied to the atoms.
    bond_thickness : float
        Used to manipulate the thickness of bonds (i.e. thickness of tubes
        which are used to render bonds)
    """
    if molecule_mapper.bonds_data_available:
        molecule_mapper_render_atoms(molecule_mapper, True)
        molecule_mapper_render_bonds(molecule_mapper, True)
        set_bond_thickness(molecule_mapper, bond_thickness/10)
        set_atomic_radius_type(molecule_mapper, 'Unit')
        set_atomic_radius_scale(molecule_mapper, bond_thickness/10)
    else:
        print("Inadequate Bonding data")

    set_atom_colormode(molecule_mapper, colormode)
    set_bond_colormode(molecule_mapper, colormode)


class PeriodicTable(vtk.vtkPeriodicTable):
    """ A class to obtain properties of elements (eg: Covalent Radius,
    Van Der Waals Radius, Symbol etc.).

    This is a more pythonic version of ``vtkPeriodicTable`` providing simple
    methods to access atomic properties. It provides access to essential
    functionality available in ``vtkPeriodicTable``. An object of this class
    provides access to atomic information sourced from Blue Obelisk Data
    Repository.
    """

    def get_atomic_symbol(self, atomic_number):
        """Given an atomic number, returns the symbol associated with the
        element.

        Parameters
        ----------
        atomic_number : int
            Atomic number of the element whose symbol is to be obtained.
        """
        return self.GetSymbol(atomic_number)

    def get_element_name(self, atomic_number):
        """Given an atomic number, returns the name of the element.

        Parameters
        ----------
        atomic_number : int
            Atomic number of the element whose name is to be obtained.
        """
        return self.GetElementName(atomic_number)

    def get_atomic_number(self, element_name):
        """Given a case-insensitive string that contains the symbol or name of
        an element, return the corresponding atomic number.

        Parameters
        ----------
        element_name : string
            Name of the element whose atomic number is to be obtained.
        """
        return self.GetAtomicNumber(element_name)

    def get_atomic_radius(self, atomic_number, radius_type):
        """Given an atomic number, return either the covalent radius of the
        atom or return the Van Der Waals radius of the atom depending on
        radius_type.

        Parameters
        ----------
        atomic_number : int
            Atomic number of the element whose covalent radius is to be
            obtained.
        radius_type : string
            Two valid choices -
            * 'VDW' : for Van Der Waals radius of the atom
            * 'Covalent' : for covalent radius of the atom
        """
        if radius_type == 'VDW':
            return self.GetVDWRadius(atomic_number)
        elif radius_type == 'Covalent':
            return self.GetCovalentRadius(atomic_number)

    def get_atom_color(self, atomic_number):
        """Given an atomic number, return the RGB tuple associated with that
        element (CPK coloring convention) provided by the Blue Obelisk Data
        Repository.

        Parameters
        ----------
        atomicNumber : int
            Atomic number of the element whose RGB tuple is to be obtained.
        """
        return self.GetDefaultRGBTuple(atomic_number)


def make_molecularviz_aesthetic(molecule_actor):
    """Manipulating the lighting to make the molecular visualization
    aesthetically pleasant to see.

    Parameters
    ----------
    molecule_actor : vtkActor
        Actor that represents the molecule to be visualized.
    """
    molecule_actor.GetProperty().SetDiffuse(1)
    molecule_actor.GetProperty().SetSpecular(0.5)
    molecule_actor.GetProperty().SetSpecularPower(90.0)


def molecular_sphere_rep_actor(molecule, colormode='discrete'):
    """Create an actor for sphere molecular representation. It's also referred
    to as CPK model and space-filling model.

    Parameters
    ----------
    molecule : Molecule() object
        The molecule to be rendered.
    colormode : string
        Set the colormode for coloring the atoms. Two valid color modes -
        * 'discrete': Atoms are colored using CPK coloring convention.
        * 'single': All atoms are colored with same color(grey).

        RGB tuple used for coloring the atoms when 'single' colormode is
        selected: (150, 150, 150)
        Default is 'discrete'.

    Returns
    -------
    molecule_actor : vtkActor
        Actor created to render the space filling representation of the
        molecule to be visualized.
    """
    msp_mapper = MoleculeMapper()
    set_molecule_to_mapper(msp_mapper, molecule)
    config_mapper_to_molecular_sphere(msp_mapper, colormode)
    molecule_actor = vtk.vtkActor()
    molecule_actor.SetMapper(msp_mapper)
    make_molecularviz_aesthetic(molecule_actor)
    return molecule_actor


def molecular_bstick_rep_actor(molecule, colormode='discrete',
                               atom_scale_factor=0.3, bond_thickness=1,
                               multiple_bonds='On'):
    """Create an actor for ball and stick molecular representation.

    Parameters
    ----------
    molecule : Molecule() object
        The molecule to be rendered.
    colormode : string
        Set the colormode for coloring the atoms. Two valid color modes -
        * 'discrete': Atoms and bonds are colored using CPK coloring
          convention.
        * 'single': All atoms are colored with same color(grey) and all bonds
          are colored with same color(dark grey).
        * RGB tuple used for coloring the atoms when 'single' colormode is
        selected: (150, 150, 150)
        * RGB tuple used for coloring the bonds when 'single' colormode is
        selected: (50, 50, 50)
        * Default is 'discrete'.

    atom_scale_factor : float
        Scaling factor colormode='discrete',
                               atom_scale_factor=0.3, bond_thickness=1,
                               multipleBoto be applied to the atoms.
        Default is 0.3.
    bond_thickness : float
        Used to manipulate the thickness of bonds (i.e. thickness of tubes
        which are used to render bonds)
        Default is 1.
    multipleBonds : string
        Set whether multiple tubes will be used to represent multiple
        bonds. Two valid choices -
        * 'On': multiple bonds (double, triple) will be shown by using
          multiple tubes.
        * 'Off': all bonds (single, double, triple) will be shown as single
          bonds (i.e shown using one tube each).
        Default is 'On'.

    Returns
    -------
    molecule_actor : vtkActor
        Actor created to render the ball and stick representation of the
        molecule to be visualized.
    """
    bs_mapper = MoleculeMapper()
    set_molecule_to_mapper(bs_mapper, molecule)
    config_mapper_to_ball_stick(bs_mapper, colormode, atom_scale_factor,
                                bond_thickness, multiple_bonds)
    molecule_actor = vtk.vtkActor()
    molecule_actor.SetMapper(bs_mapper)
    make_molecularviz_aesthetic(molecule_actor)
    return molecule_actor


def molecular_stick_rep_actor(molecule, colormode='discrete',
                              bond_thickness=1):
    """Create an actor for stick molecular representation.

    Parameters
    ----------
    molecule : Molecule object
        The molecule to be rendered.
    colormode : string
        Set the colormode for coloring the bonds. Two valid color modes -
        * 'discrete': Bonds are colored using CPK coloring convention.
        * 'single': All bonds are colored with the same color (dark grey)
        RGB tuple used for coloring the bonds when 'single' colormode is
        selected: (50, 50, 50)
        Default is 'discrete'.

    bond_thickness : float
        Used to manipulate the thickness of bonds (i.e. thickness of tubes
        which are used to render bonds).
        Default is 1.

    Returns
    -------
    molecule_actor : vtkActor
        Actor created to render the stick representation of the molecule to be
        visualized.
    """
    mst_mapper = MoleculeMapper()
    set_molecule_to_mapper(mst_mapper, molecule)
    config_mapper_to_stick(mst_mapper, colormode, bond_thickness)
    molecule_actor = vtk.vtkActor()
    molecule_actor.SetMapper(mst_mapper)
    make_molecularviz_aesthetic(molecule_actor)
    return molecule_actor
