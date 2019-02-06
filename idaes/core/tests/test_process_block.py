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
Tests ProcessBlock and ProcessBlockData.

Author: John Eslick
"""
import pytest
from pyomo.environ import ConcreteModel, Var, value
from pyomo.common.config import ConfigValue
from idaes.core import (
    ProcessBlock,
    ProcessBlockData,
    declare_process_block_class)


@declare_process_block_class("MyBlock")
class MyBlockData(ProcessBlockData):
    CONFIG = ProcessBlockData.CONFIG()
    CONFIG.declare("xinit", ConfigValue(default=1001, domain=float))
    CONFIG.declare("yinit", ConfigValue(default=1002, domain=float))
    def build(self):
        super(MyBlockData, self).build()
        self.x = Var(initialize=self.config.xinit)
        self.y = Var(initialize=self.config.yinit)


class TestProcessBlock(object):
    def test_scalar_noargs(self):
        m = ConcreteModel()
        m.b = MyBlock()
        assert(isinstance(m.b.x, Var))
        assert(isinstance(m.b.y, Var))
        assert(value(m.b.x) == 1001)
        assert(value(m.b.y) == 1002)

    def test_vec_noargs(self):
        m = ConcreteModel()
        m.b = MyBlock([1,2,3])
        assert(isinstance(m.b[1].x, Var))
        assert(isinstance(m.b[1].y, Var))
        assert(isinstance(m.b[2].x, Var))
        assert(isinstance(m.b[2].y, Var))
        assert(isinstance(m.b[3].x, Var))
        assert(isinstance(m.b[3].y, Var))
        assert(value(m.b[1].x) == 1001)
        assert(value(m.b[1].y) == 1002)
        assert(value(m.b[2].x) == 1001)
        assert(value(m.b[2].y) == 1002)
        assert(value(m.b[3].x) == 1001)
        assert(value(m.b[3].y) == 1002)

    def test_scalar_args1(self):
        m = ConcreteModel()
        m.b = MyBlock(default={"xinit":1, "yinit":2})
        assert(isinstance(m.b.x, Var))
        assert(isinstance(m.b.y, Var))
        assert(value(m.b.x) == 1)
        assert(value(m.b.y) == 2)

    def test_scalar_args2(self):
        m = ConcreteModel()
        m.b = MyBlock(initialize={None:{"xinit":1, "yinit":2}})
        assert(isinstance(m.b.x, Var))
        assert(isinstance(m.b.y, Var))
        assert(value(m.b.x) == 1)
        assert(value(m.b.y) == 2)

    def test_vec_args(self):
        m = ConcreteModel()
        m.b = MyBlock(
            [1,2,3],
            default={"xinit":1, "yinit":2},
            initialize={2:{"xinit":2001, "yinit":2002}})
        assert(isinstance(m.b[1].x, Var))
        assert(isinstance(m.b[1].y, Var))
        assert(isinstance(m.b[2].x, Var))
        assert(isinstance(m.b[2].y, Var))
        assert(isinstance(m.b[3].x, Var))
        assert(isinstance(m.b[3].y, Var))
        assert(m.b[1].index() == 1)
        assert(value(m.b[1].x) == 1)
        assert(value(m.b[1].y) == 2)
        assert(value(m.b[2].x) == 2001)
        assert(value(m.b[2].y) == 2002)
        assert(value(m.b[3].x) == 1)
        assert(value(m.b[3].y) == 2)