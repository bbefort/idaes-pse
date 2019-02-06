##############################################################################
# Institute for the Design of Advanced Energy Systems Process Systems
# Engineering Framework (IDAES PSE Framework) Copyright (c) 2018-2019, by the
# software owners: The Regents of the University of California, through
# Lawrence Berkeley National Laboratory,  National Technology & Engineering
# Solutions of Sandia, LLC, Carnegie Mellon University, West Virginia
# University Research Corporation, et al. All rights reserved.
#
# Please see the files COPYRIGHT.txt and LICENSE.txt for full copyright and
# license information, respectively. Both files are also available online
# at the URL "https://github.com/IDAES/idaes-pse".
##############################################################################
"""
Tests that tutorials run.

Author: Andrew Lee
"""
import pytest
from pyomo.environ import SolverFactory
from pyomo.opt import SolverStatus, TerminationCondition
from idaes.ui.report import degrees_of_freedom

# Import file to be tested
from os.path import abspath, dirname, join
from pyutilib.misc import import_file
example = join(dirname(abspath(__file__)), '..', '..', 'examples', 'tutorials')


# See if ipopt is available and set up solver
if not SolverFactory('ipopt').available():
    solver = None
else:
    solver = True


@pytest.mark.skipif(solver is None, reason="Solver not available")
def test_tutorial_1():
    f = import_file(join(example, "Tutorial_1_Basic_Flowsheets"))
    m, results = f.main()

    # Check for optimal solution
    assert results.solver.termination_condition == TerminationCondition.optimal
    assert results.solver.status == SolverStatus.ok

    assert degrees_of_freedom(m) == 0

    assert (m.fs.Tank2.outlet[0].flow_vol.value ==
            pytest.approx(1.0, abs=1e-2))
    assert (m.fs.Tank2.outlet[0].conc_mol_comp["Ethanol"].value ==
            pytest.approx(89.628, abs=1e-2))
    assert (m.fs.Tank2.outlet[0].conc_mol_comp["EthylAcetate"].value ==
            pytest.approx(10.372, abs=1e-2))
    assert (m.fs.Tank2.outlet[0].conc_mol_comp["NaOH"].value ==
            pytest.approx(10.372, abs=1e-2))
    assert (m.fs.Tank2.outlet[0].conc_mol_comp["SodiumAcetate"].value ==
            pytest.approx(89.628, abs=1e-2))
    assert (m.fs.Tank2.outlet[0].conc_mol_comp["H2O"].value ==
            pytest.approx(55388.0, abs=1))
    assert (m.fs.Tank2.outlet[0].pressure.value ==
            pytest.approx(101325, abs=1))
    assert (m.fs.Tank2.outlet[0].temperature.value ==
            pytest.approx(304.20, abs=1e-1))


@pytest.mark.skipif(solver is None, reason="Solver not available")
def test_tutorial_2():
    f = import_file(join(example, "Tutorial_2_Basic_Flowsheet_Optimization"))
    m, results = f.main()

    # Check for optimal solution
    assert results.solver.termination_condition == TerminationCondition.optimal
    assert results.solver.status == SolverStatus.ok

    assert degrees_of_freedom(m) == 1

    assert (m.fs.Tank2.outlet[0].flow_vol.value ==
            pytest.approx(1.0, abs=1e-2))
    assert (m.fs.Tank2.outlet[0].conc_mol_comp["Ethanol"].value ==
            pytest.approx(92.106, abs=1e-2))
    assert (m.fs.Tank2.outlet[0].conc_mol_comp["EthylAcetate"].value ==
            pytest.approx(7.894, abs=1e-2))
    assert (m.fs.Tank2.outlet[0].conc_mol_comp["NaOH"].value ==
            pytest.approx(7.894, abs=1e-2))
    assert (m.fs.Tank2.outlet[0].conc_mol_comp["SodiumAcetate"].value ==
            pytest.approx(92.106, abs=1e-2))
    assert (m.fs.Tank2.outlet[0].conc_mol_comp["H2O"].value ==
            pytest.approx(55388.0, abs=1))
    assert (m.fs.Tank2.outlet[0].pressure.value ==
            pytest.approx(101325, abs=1))
    assert (m.fs.Tank2.outlet[0].temperature.value ==
            pytest.approx(304.23, abs=1e-1))

    assert (m.fs.Tank1.volume[0].value == pytest.approx(1.215, abs=1e-2))
    assert (m.fs.Tank2.volume[0].value == pytest.approx(1.785, abs=1e-2))