""" Functions regarding PPRs. """

def ppr_tr(nper, standard_withdrawal):
    """
    Get the tax rate applied on the PPR capital gains.

    Given:
     * the total number of compounding periods, ``nper``,
     * and whether the PPR will be withdrawn in standard conditions or not,
       ``standard_withdrawal``.

    Return:
       The tax rate applied on the PPR capital gains.

    Parameters
    ----------
    nper : scalar
        Number of compounding periods
    standard_withdrawal : bool
        Whether the PPR will be withdrawn in standard conditions or not.

    Returns
    -------
    out : scalar
        The tax rate applied on the PPR capital gains.

    Notes
    -----
    At the time of writing, PPR capital gains are taxed at 8% if the investment is
    withdrew in the situations foreseen by law. In non-standard situations, the tax
    rate applied depends on the time the investment was held, as follows:

    - Holding for less than 5 years: 21.5%

    - Holding between 5 and 8 years: 17.2%

    - Holding for 8 or more years: 8.6%

    Examples
    --------
    >>> import pyppr
    >>> holding_periods = [4, 5, 7, 8, 9]
    >>> trs = [pyppr.ppr_tr(period, False) for period in holding_periods]
    >>> print('In non-standard withdrawals, PPR capital gains are taxed at:')
    >>> for period, tr in zip(holding_periods, trs):
    ...     print(f'- {tr:.1%} in a {period}-year investment.')
    In non-standard withdrawals, PPR capital gains are taxed at:
    - 21.5% in a 4-year investment.
    - 17.2% in a 5-year investment.
    - 17.2% in a 7-year investment.
    - 8.6% in a 8-year investment.
    - 8.6% in a 9-year investment.

    """

    return 0.08 if standard_withdrawal else 0.215 if nper < 5 else 0.172 if nper < 8 else 0.086


def ppr_net_fv(ua_cagr, nper, pv, ppr_costr, ppr_tcr, ppr_standard_withdrawal):
    """
    Compute the final tax-net value of a PPR.

    Given:
     * the CAGR of the PPR's underlying assets, ``ua_cagr``, compounded once per
       period, of which there are
     * ``nper`` total,
     * the initial invested capital, ``pv``, often referred to as the present value,
     * the PPR's total costs, ``ppr_costr``, including its management commission and
       others, expressed as a percentage of the invested capital,
     * the tax credit rate, ``ppr_tcr``, the investor gets in his IRS for
       investing in a PPR,
     * and whether the PPR will be withdrawn in standard conditions or not,
       ``ppr_standard_withdrawal``.

    Return:
       The tax-net value of a PPR at the end of the investment.

    Parameters
    ----------
    ua_cagr : scalar or array_like of shape(M, )
        Cumulative annual growth rate of the PPR's underlying assets, in percentage
        Example: 0.05
    nper : scalar or array_like of shape(M, )
        Number of compounding periods
    pv : scalar or array_like of shape(M, )
        Initial invested capital, often referred to as the present value
    ppr_costr : scalar or array_like of shape(M, )
        PPR's total costs, including its management commission and others, expressed
        as a percentage of the invested capital
        Example: 0.0075
    ppr_tcr : scalar or array_like of shape(M, )
        Tax credit rate the investor gets in his IRS for investing in a PPR
        Example: 0 or 0.2
    ppr_standard_withdrawal : bool
        Whether the PPR will be withdrawn in standard conditions or not.

    Returns
    -------
    out : array_like
        Final tax-net value of a PPR. If all input is scalar, returns a scalar float.
        If any input is array_like, returns the annual cost rate for each input
        element.

    Warnings
    --------_
    ``ppr_net_fv`` considers the PPR's tax credit is reinvested into the PPR, itself
    not generating any tax credit.

    Notes
    -----
    Returns the result of

    .. math::
        V_0 + (PPR_n - V_0)\\,(1 - tr_{PPR}) + TC_0 + (TC_n - TC_0)\\,(1 - tr_{PPR})

    which, according to :ref:`The Math Behind the Functions <math-behind-functions>`,
    in its longest form, can be decomposed to

    .. math:: 
        V_0\\,(1 + tcp_{PPR})\\,(1 + r)^n\\,(1 - cr_{PPR})^n\\,(1 - tr_{PPR})
        + V_0\\,(1 + tcp_{PPR})\\,(tr_{PPR})

    You should take care to define the PPR's tax credit rate according to the law.
    We recommend you to only consider inputting 0 or the current credit rate (at the
    time of this writing, 0.2) in the :math:`ppr_{tcr}` parameter, even if only part
    of the investment will generate the credit. In that case, split the investment
    into two parts, one with :math:`ppr_{tcr}` = 0 and the other with
    :math:`ppr_{tcr} = 0.2`.

    Examples
    --------
    >>> import pyppr

    What will be the final value of an investment in the a PPR, under the following
    scenario?

    - I expect the PPR's underlying assets to grow at a CAGR of 7%.

    - I expect to hold this investment for the next 30 years.

    - I'm investing 4,000€.

    - I'm 30 years old, which means I can receive a tax credit of up to 400€.

    - This PPR charges a management commission of 0.75% per year, and no other costs.

    - I'm going to withdraw the PPR under standard conditions.

    >>> fv1 = pyppr.ppr_net_fv(0.07, 20, 2000, 0.0075, 0.2, True)
    >>> fv2 = pyppr.ppr_net_fv(0.07, 20, 2000, 0.0075, 0, True)
    >>> print(f'{fv1 + fv2:,.2f} ({fv1:,.2f} + {fv2:,.2f})')
    13,826.93 (7,541.96 + 6,284.97)

    Or, alternatively,

    >>> fv = pyppr.ppr_net_fv(0.07, 20, 2000, 0.0075, np.array([0.2, 0]), True)
    >>> print(f'{fv.sum():,.2f} ({fv[0]:,.2f} + {fv[1]:,.2f})')
    13,826.93 (7,541.96 + 6,284.97)

    If we were investing 5,000€ instead,

    >>> import numpy as np
    >>> fv = pyppr.ppr_net_fv(0.07, 20, np.array([2000, 3000]), 0.0075, np.array([0.2, 0]), True)
    >>> print(f'{fv.sum():,.2f} ({fv[0]:,.2f} + {fv[1]:,.2f})')
    16,969.41 (7,541.96 + 9,427.45)

    """

    _ppr_tr = ppr_tr(nper, ppr_standard_withdrawal)

    return pv * (1 + ppr_tcr) * (1 + ua_cagr) ** nper * (1 - ppr_costr) ** nper * (1 - _ppr_tr) + \
        pv * (1 + ppr_tcr) * _ppr_tr


def matching_ppr_cost_rate(ua_cagr, nper, ua_tr, ppr_ev, ppr_tcr, ppr_standard_withdrawal):
    """
    Compute the PPR annual cost rate that makes the PPR's tax-net final value
    match that of an investment in its underlying assets, with a defined extra
    return.

    Given:
     * the CAGR of the PPR's underlying assets, ``ua_cagr``, compounded once per
       period, of which there are
     * ``nper`` total,
     * the tax rate, ``ua_tr``, the investor would pay on the capital gains in the
       underlying assets, had he invested in them directly,
     * the tax credit rate, ``ppr_tcr``, the investor gets in his IRS for investing
       in a PPR,
     * the extra after-tax value, ``ppr_ev``, the PPR can/should generate comparing
       to its underlying assets. Expressed in percentage and can be negative,
     * and whether the PPR will be withdrawn in standard conditions or not,
       ``ppr_standard_withdrawal``.

    Return:
       The PPR annual cost rate that makes the PPR and an investment in its
       underlying assets generate the same tax-net final value, plus/minus the
       defined extra return.

    Parameters
    ----------
    ua_cagr : scalar or array_like of shape(M, )
        Cumulative annual growth rate of the PPR's underlying assets, in percentage
        Example: 0.05
    nper : scalar or array_like of shape(M, )
        Number of compounding periods
    ua_tr : scalar or array_like of shape(M, )
        Tax rate the investor would pay on the capital gains in the underlying assets
        Example: 0.28
    ppr_ev : scalar or array_like of shape(M, )
        PPR's extra after-tax final value comparing to its underlying assets
        Example: -0.03 means that the final after-tax investment value generated by
        the PPR is 3% less than that of an investment made directly in the PPR's
        underlying assets
    ppr_tcr : scalar or array_like of shape(M, )
        Tax credit rate the investor gets in his IRS for investing in a PPR
        Example: 0 or 0.2
    ppr_standard_withdrawal : bool
        Whether the PPR will be withdrawn in standard conditions or not.
        
    Returns
    -------
    out : array_like
        PPR annual cost rate. If all input is scalar, returns a scalar float. If any
        input is array_like, returns the annual cost rate for each input element.

    Warnings
    --------_
    ``matching_ppr_cost_rate`` considers the PPR's tax credit is reinvested into the
    PPR, itself not generating any tax credit.

    See Also
    --------
    matching_underlying_assets_cagr, matching_ppr_extra_value

    Notes
    -----
    Returns the result of

    .. math::
       V_0 + (PPR_n - V_0)\\,(1 - tr_{PPR}) + TC_0 + (TC_n - TC_0)\\,(1 - tr_{PPR})
       = [ \\, V_0 + (UA_n - V_0)\\,(1 - tr_{UA}) \\, ] \\, (1 + ev_{PPR})

    which, according to :ref:`The Math Behind the Functions <math-behind-functions>`,
    in its longest form, can be decomposed to

    .. math::
       V_0\\,(1 + tcp_{PPR})\\,(1 + r)^n\\,(1 - cr_{PPR})^n\\,(1 - tr_{PPR})
       + V_0\\,(1 + tcp_{PPR})\\,(tr_{PPR})
       = V_0\\,(1 + r)^n\\,(1-tr_{ETF})\\,(1 + ev_{PPR}) + V_0\\,(tr_{ETF})\\,(1 + ev_{PPR})

    solved to :math:`cr_{PPR}`, which gives the following formula:

    .. math::
       cr_{PPR} = 1 - \\sqrt[n]{\\frac{(1+r)^n\\,(1-tr_{UA})\\,(1 + ev_{PPR}) +
       tr_{UA}\\,(1 + ev_{PPR}) - tr_{PPR}\\,(1 + tcp_{PPR})}
       {(1 + r)^n\\,(1 + tcp_{PPR})(1 - tr_{PPR})}}

    You should take care to define the PPR's tax credit rate according to the law.
    We recommend you to only consider inputting 0 or the current credit rate (at the
    time of this writing, 0.2) in the :math:`ppr_{tcr}` parameter, even if only part
    of the investment will generate the credit. In that case, split the investment
    into two parts, one with :math:`ppr_{tcr}` = 0 and the other with
    :math:`ppr_{tcr} = 0.2`.

    Examples
    --------
    >>> import pyppr

    There's a PPR that tracks the ETF I'm interested in investing in. Should I invest in
    the PPR or directly in the ETF? Here's the scenario:

    - I expect the ETF to grow at a CAGR of 7%.

    - I expect to hold this investment for the next 20 years.

    - When withdrawing, I expect to pay 28% on capital gains.

    - Given the limitations and hurdles of the PPR, I require it to generate an extra 8%
      return, to choose it over the ETF.

    - I already invest in another ETF and I max out my tax credit when investing in it.

    - This PPR charges a management commission of 0.75% per year, and no other costs.

    - I will withdraw the PPR under standard conditions.

    >>> match = pyppr.matching_ppr_cost_rate(0.07, 20, 0.28, 0.08, 0, True)
    >>> if ( match < 0.0075 ):
    ...     print('I should invest directly in the underlying assets.')
    >>> else:
    ...     print('I should invest in the PPR.')

    What range would the PPR's cost rate have to be in, for it to deliver somewhere
    between 6% and 9% extra value than investing in its underlying assets directly?

    >>> import numpy as np
    >>> matches = pyppr.matching_ppr_cost_rate(0.07, 20, 0.28, np.array([0.06, 0.09]), 0, True)
    >>> print(matches)
    [0.00578394 0.00436104]
    >>> print(f'{matches[1]:.2%} - {matches[0]:.2%}')
    0.44% - 0.58%

    """

    _ppr_tr = ppr_tr(nper, ppr_standard_withdrawal)

    return 1 - \
        (
            (
                (1 + ua_cagr) ** nper * (1 - ua_tr) * (1 + ppr_ev) +
                ua_tr * (1 + ppr_ev) -
                _ppr_tr * (1 + ppr_tcr)
            ) /
            (
                (1 + ua_cagr) ** nper * (1 + ppr_tcr) * (1 - _ppr_tr)
            )
        ) ** (1 / nper)


def matching_underlying_assets_cagr(nper, ua_tr, ppr_ev, ppr_costr, ppr_tcr, ppr_standard_withdrawal):
    """
    Compute the Cumulative Annual Growth Rate (CAGR) of the PPR's Underlying Assets
    that makes the PPR's tax-net final value match that of an investment in the
    underlying assets, with a defined extra return.

    Given:
     * the total number of compounding periods, ``nper``,
     * the tax rate, ``ua_tr``, the investor would pay on the capital gains in the
       underlying assets, had he invested in them directly,
     * the PPR's total costs, ``ppr_costr``, including its management commission and
       others, expressed as a percentage of the invested capital,
     * the tax credit rate, ``ppr_tcr``, the investor gets in his IRS for investing
       in a PPR,
     * the extra after-tax value, ``ppr_ev``, the PPR can/should generate
       comparing to its underlying assets. Expressed in percentage and can be
       negative,
     * and whether the PPR will be withdrawn in standard conditions or not,
       ``ppr_standard_withdrawal``.

    Return:
       The Underlying Assets' CAGR that makes the PPR and an investment in its
       underlying assets generate the same tax-net final value, plus/minus the
       defined extra return.

    Parameters
    ----------
    nper : scalar or array_like of shape(M, )
        Number of compounding periods
    ua_tr : scalar or array_like of shape(M, )
        Tax rate the investor would pay on the capital gains in the underlying assets
        Example: 0.28
    ppr_ev : scalar or array_like of shape(M, )
        PPR's extra after-tax final value comparing to its underlying assets
        Example: -0.03 means that the final after-tax investment value generated by
        the PPR is 3% less than that of an investment made directly in the PPR's
        underlying assets
    ppr_costr : scalar or array_like of shape(M, )
        PPR's total costs, including its management commission and others, expressed
        as a percentage of the invested capital
        Example: 0.0075
    ppr_tcr : scalar or array_like of shape(M, )
        Tax credit rate the investor gets in his IRS for investing in a PPR
        Example: 0 or 0.2
    ppr_standard_withdrawal : bool
        Whether the PPR will be withdrawn in standard conditions or not.

    Returns
    -------
    out : array_like
        The Underlying Assets' CAGR. If all input is scalar, returns a scalar float.
        If any input is array_like, returns the annual cost rate for each input
        element.

    Warnings
    --------
    ``matching_underlying_assets_cagr`` considers the PPR's tax credit is reinvested
    into the PPR, itself not generating any tax credit.

    See Also
    --------
    matching_ppr_cost_rate, matching_ppr_extra_value

    Notes
    -----
    Returns the result of

    .. math::
       V_0 + (PPR_n - V_0)\\,(1 - tr_{PPR}) + TC_0 + (TC_n - TC_0)\\,(1 - tr_{PPR})
       = [ \\, V_0 + (UA_n - V_0)\\,(1 - tr_{UA}) \\, ] \\, (1 + ev_{PPR})

    which, according to :ref:`The Math Behind the Functions <math-behind-functions>`,
    in its longest form, can be decomposed to

    .. math::
       V_0\\,(1 + tcp_{PPR})\\,(1 + r)^n\\,(1 - cr_{PPR})^n\\,(1 - tr_{PPR})
       + V_0\\,(1 + tcp_{PPR})\\,(tr_{PPR})
       = V_0\\,(1 + r)^n\\,(1-tr_{ETF})\\,(1 + ev_{PPR}) + V_0\\,(tr_{ETF})\\,(1 + ev_{PPR})

    solved to :math:`r`, which gives the following formula:

    .. math::
       r = \\sqrt[n]{\\frac{tr_{ETF}\\,(1 + ev_{PPR}) - tr_{PPR}\\,(1 + tcp_{PPR})}
       {(1-cr_{PPR})^n\\,(1+tcp_{PPR})\\,(1 - tr_{PPR}) - (1-tr_{ETF})\\,(1 + ev_{PPR})}} - 1

    You should take care to define the PPR's tax credit rate according to the law.
    We recommend you to only consider inputting 0 or the current credit rate (at the
    time of this writing, 0.2) in the :math:`ppr_{tcr}` parameter, even if only part
    of the investment will generate the credit. In that case, split the investment
    into two parts, one with :math:`ppr_{tcr}` = 0 and the other with
    :math:`ppr_{tcr} = 0.2`.

    Examples
    --------
    >>> import pyppr

    There's a PPR that tracks the ETF I'm interested in investing in. Should I invest in
    the PPR or directly in the ETF? Here's the scenario:

    - I expect to hold this investment for the next 20 years.

    - During that time, I expect the ETF to grow at a CAGR of 7%.

    - When withdrawing, I expect to pay 28% on capital gains.

    - Given the limitations and hurdles of the PPR, I require it to generate an extra 8%
      return, to choose it over the ETF.

    - I already invest in another ETF and I max out my tax credit when investing in it.

    - This PPR charges a management commission of 0.75% per year, and no other costs.

    - I will withdraw the PPR under standard conditions.

    >>> match = pyppr.matching_underlying_assets_cagr(20, 0.28, 0.08, 0.0075, 0, True)
    >>> if ( match >= 0.007 ):
    ...     print('I should invest directly in the underlying assets.')
    >>> else:
    ...     print('I should invest in the PPR.')

    We can make this decision by comparing the matching CAGR with our expectation of
    it because we know that higher CAGRs make PPRs more attractive than investing
    directly in its underlying assets. This is because higher CAGRs make the PPR's
    costs lower and the tax benefits higher in relative terms.

    What range would the PPR's cost rate have to be in, for it to deliver somewhere
    between 6% and 9% extra value than investing in its underlying assets directly?

    >>> import numpy as np
    >>> years = np.array([10, 20, 30])
    >>> match = pyppr.matching_underlying_assets_cagr(years, 0.28, 0.08, 0.0075, 0, True)
    >>> for year, match in zip(years, matches):
    ...     if np.isnan(match):
    ...         print(f'A PPR with 0.75% yearly cost cannot provide 8% more value for a {year}-year investment.')
    ...     else:
    ...         print(f'A {match:.2%} CAGR is required for a {year}-year investment.')
    A 11.38% CAGR is required for a 10-year investment.
    A 14.91% CAGR is required for a 20-year investment.
    A PPR with 0.75% yearly cost cannot provide 8% more value for a 30-year investment.

    """

    _ppr_tr = ppr_tr(nper, ppr_standard_withdrawal)

    return (
            (
                ua_tr * (1 + ppr_ev) - _ppr_tr * (1 + ppr_tcr)
            ) /
            (
                (1 - ppr_costr) ** nper * (1 + ppr_tcr) * (1 - _ppr_tr) - (1 - ua_tr) * (1 + ppr_ev)
            )
        ) ** (1 / nper) - 1


def matching_ppr_extra_value(ua_cagr, nper, ua_tr, ppr_costr, ppr_tcr, ppr_standard_withdrawal):
    """
    Compute the after-tax extra value, expressed as a (positive or negative)
    percentage, generated by a PPR comparing to an investment made directly its
    Underlying Assets.

    Given:
     * the CAGR of the PPR's underlying assets, ``ua_cagr``, compounded once per
       period, of which there are
     * ``nper`` total,
     * the tax rate, ``ua_tr``, the investor would pay on the capital gains in the
       underlying assets, had he invested in them directly,
     * the PPR's total costs, ``ppr_costr``, including its management commission and
       others, expressed as a percentage of the invested capital,
     * the tax credit rate, ``ppr_tcr``, the investor gets in his IRS for
       investing in a PPR,
     * and whether the PPR will be withdrawn in standard conditions or not,
       ``ppr_standard_withdrawal``.

    Return:
       The difference between the PPR's and its Underlying Assets' tax-net final
       value.

    Parameters
    ----------
    ua_cagr : scalar or array_like of shape(M, )
        Cumulative annual growth rate of the PPR's underlying assets, in percentage
        Example: 0.05
    nper : scalar or array_like of shape(M, )
        Number of compounding periods
    ua_tr : scalar or array_like of shape(M, )
        Tax rate the investor would pay on the capital gains in the underlying assets
        Example: 0.28
    ppr_costr : scalar or array_like of shape(M, )
        PPR's total costs, including its management commission and others, expressed
        as a percentage of the invested capital
        Example: 0.0075
    ppr_tcr : scalar or array_like of shape(M, )
        Tax credit rate the investor gets in his IRS for investing in a PPR
        Example: 0 or 0.2
    ppr_standard_withdrawal : bool
        Whether the PPR will be withdrawn in standard conditions or not.

    Returns
    -------
    out : array_like
        The after-tax extra value generated by the PPR, in percentage.

    Warnings
    --------_
    ``matching_ppr_extra_value`` considers the PPR's tax credit is reinvested
    into the PPR, itself not generating any tax credit.

    See Also
    --------
    matching_ppr_cost_rate, matching_underlying_assets_cagr

    Notes
    -----
    Returns the result of

    .. math::
       V_0 + (PPR_n - V_0)\\,(1 - tr_{PPR}) + TC_0 + (TC_n - TC_0)\\,(1 - tr_{PPR})
       = [ \\, V_0 + (UA_n - V_0)\\,(1 - tr_{UA}) \\, ] \\, (1 + ev_{PPR})

    which, according to :ref:`The Math Behind the Functions <math-behind-functions>`,
    in its longest form, can be decomposed to

    .. math::
       ,V_0\\,(1 + tcp_{PPR})\\,(1 + r)^n\\,(1 - cr_{PPR})^n\\,(1 - tr_{PPR})
       + V_0\\,(1 + tcp_{PPR})\\,(tr_{PPR})
       = V_0\\,(1 + r)^n\\,(1-tr_{ETF})\\,(1 + ev_{PPR}) + V_0\\,(tr_{ETF})\\,(1 + ev_{PPR})

    solved to :math:`ev_{PPR}`, which gives the following formula:

    .. math::
       ev_{PPR} = \\frac{(1 + r)^n\\,(1 - cr_{PPR})^n\\,(1 + tcp_{PPR})\\,(1 - tr_{PPR})
       + tr_{PPR}\\,(1 + tcp_{PPR})}
       {(1 + r)^n\\,(1 - tr_{ETF})+tr_{ETF}} - 1

    You should take care to define the PPR's tax credit rate according to the law.
    We recommend you to only consider inputting 0 or the current credit rate (at the
    time of this writing, 0.2) in the :math:`ppr_{tcr}` parameter, even if only part
    of the investment will generate the credit. In that case, split the investment
    into two parts, one with :math:`ppr_{tcr}` = 0 and the other with
    :math:`ppr_{tcr} = 0.2`.

    Examples
    --------
    >>> import pyppr

    There's a PPR that tracks the ETF I'm interested in investing in. Should I invest in
    the PPR or directly in the ETF? Here's the scenario:

    - I expect the ETF to grow at a CAGR of 7%.

    - I expect to hold this investment for the next 20 years.

    - When withdrawing, I expect to pay 28% on capital gains.

    - Given the limitations and hurdles of the PPR, I require it to generate an extra 8%
      return, to choose it over the ETF.

    - I already invest in another ETF and I max out my tax credit when investing in it.

    - This PPR charges a management commission of 0.75% per year, and no other costs.

    - I will withdraw the PPR under standard conditions.
    
    >>> match = pyppr.matching_ppr_extra_value(0.07, 20, 0.28, 0.0075, 0, True)
    >>> if ( match < 0.08 ):
    ...     print('I should invest directly in the underlying assets.')
    >>> else:
    ...     print('I should invest in the PPR.')

    How much more tax-net value would investing in the PPR provide if we expect the
    underlying assets to grow somewhere between 6% to 8%?

    >>> import numpy as np
    >>> matches = pyppr.matching_ppr_extra_value(np.array([0.06, 0.08]), 20, 0.28, 0.0075, 0, True)
    >>> print(matches)
    [0.01120129 0.03652754]
    >>> print(f'{matches[0]:.2%} - {matches[1]:.2%}')
    1.12% - 3.65%

    """

    _ppr_tr = ppr_tr(nper, ppr_standard_withdrawal)

    return (
            (
                (1 + ua_cagr) ** nper * (1 - ppr_costr) ** nper * (1 + ppr_tcr) * (1 - _ppr_tr)
                + _ppr_tr * (1 + ppr_tcr)
            ) /
            (
                (1 + ua_cagr) ** nper * (1 - ua_tr) + ua_tr
            )
            - 1
        )
