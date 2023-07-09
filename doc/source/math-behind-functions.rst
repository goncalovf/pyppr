.. _math-behind-functions:

#############################
The Math Behind the Functions
#############################

Investment tax-net value
========================

In general, an investment's tax-net value can be calculated by

.. math::
   V_0 + (V_n - V_0)\,(1 - tr)

Where:

- :math:`V_0` is the initial value of the investment.

- :math:`V_n` is the final gross value of the investment.

- :math:`n` is the number of compounding periods (generally years).

- :math:`tr` is the tax rate applicable to that investment.

This can be simplified to

.. math::
  V_n\,(1-tr) + V_0\,tr

This applies for both the :math:`PPR` and its :math:`Underlying \; Assets`. The only
difference is the :math:`tr` applied.

Investment gross value and PPR costs
=================================================

The gross final values, :math:`V_n`, for the PPR and its Underlying Assets (UA) can
be calculated by

.. math::
   UA_n = V_0\,(1 + r)^n

and

.. math::
   PPR_n = UA_n\,(1 - cr_{PPR})^n = V_0\,(1 + r)^n\,(1 - cr_{PPR})^n

Where:

- :math:`UA_n` is the final gross value of an investment in the PPR's UA.

- :math:`PPR_n` is the final gross value of an investment in a PPR, not considering
  any tax credit.

- :math:`r` is the UA's cumulative annual growth rate (CAGR).

- :math:`cr_{PPR}` is the total PPR-specific cost incurred by the investor every
  year, expressed as a percentage of the year's investment value. It includes the
  management commission, banking fees, audits, and other costs of running the fund.

PPR Tax Benefits
================

Investment in a PPR generates a tax credit in the following year of :math:`20\%` of
the amount investment, until that amount reaches a certain limit depending on the
investor's age.

.. math::
   TC_0 = V_0 \, (tcp_{PPR})

Where:

- :math:`TC_0` is the tax credit.

- :math:`tcp_{PPR}` is the percentage of :math:`V_0` returned as tax credit. We can
  consider it as always either :math:`0` or :math:`20\%`, because even an investment
  that is not fully considered for the tax credit can be split between the portion
  that is considered in :math:`20\%` and the portion that does not generate any tax
  credit.

If we assume that :math:`TC` is invested in the PPR, we have

.. math::
   TC_n = TC_0\,(1+r)^n\,(1-mc)^n

Where:

- :math:`TC_n` is the final gross value of the investment of the tax credit in a PPR.

- :math:`TC_0` is the initial value of the tax credit.

PPR tax-net value
=================

Given the expressions above, we can get the tax-net value of an investment in a PPR as

.. math::
   V_0 + (PPR_n - V_0)\,(1 - tr_{PPR}) + TC_0 + (TC_n - TC_0)\,(1 - tr_{PPR})

.. math::
   =\,V_0\,(1 + tcp_{PPR})\,(1 + r)^n\,(1 - cr_{PPR})^n\,(1 - tr_{PPR}) + V_0\,(1 + tcp_{PPR})\,(tr_{PPR})

Supporting Excel
================

:download:`Download the Excel <_static/pyppr.xlsx>` we used to confirm the math above.

.. image:: _static/pyppr-excel-snapshot.jpg
