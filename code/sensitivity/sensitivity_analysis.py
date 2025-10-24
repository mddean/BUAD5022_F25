import pandas as pd

# Define a function that will return sensitivity analysis for the variables
def sa_vars(the_vars):
    """
    This function takes the variables from a solved model
    and returns a pandas DataFrame where the index is the
    variable name and the columns are the (1) the resulting
    value of the variable, (2) the reduced cost, (3) the
    objective function coefficient, (4) the low end of the
    range of optimality, and (5) the high end of the range
    of optimality

    Parameters
    ===============
    the_vars: the variables of the solved model (e.g., the
              result of m.getVars())

    Returns
    ===============
    A pandas DataFrame object
    """
    sa = {}
    for v in the_vars:
        sa[v.VarName] = [v.X, v.RC, v.Obj, v.SAObjLow, v.SAObjUp]

    return pd.DataFrame.from_dict(sa,
                       orient='index',
                       columns=['final_value', 'reduced_cost', 'obj_coef', 'range_opt_low', 'range_opt_high'])


# Define a function that will return sensitivity analysis for the constraints
def sa_constrs(the_constrs):
    """
    This function takes the constraints from a solved model
    and returns a pandas DataFrame where the index is the
    constraint name and the columns are the (1) indication 
    if the constraint is binding or non-binding, (2) the
    value of the constraint, (3) the RHS of the constraint,
    (4) the slack, (5) the shadow price, (6) the low end of
    the range of feasibility, and (7) the high end of the
    range of feasibility

    Parameters
    ===============
    the_constrs: the constraints of the solved model (e.g., the
              result of m.getConstrs())

    Returns
    ===============
    A pandas DataFrame object
    """
    sa = {}
    for c in the_constrs:
        binding = 'binding'
        if c.Slack > 0.00001:
            binding = 'non-binding'
        sa[c.constrName] = [binding, c.RHS-c.Slack, c.RHS, c.Slack, c.pi, c.SARHSLow, c.SARHSUp]

    return pd.DataFrame.from_dict(sa,
                        orient='index',
                        columns=['binding?', 'final_value', 'RHS', 'slack', 'shadow_price', 'range_feas_low', 'range_feas_high'])