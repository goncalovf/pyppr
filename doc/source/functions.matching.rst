.. _functions.matching:

.. currentmodule:: pyppr

Matching functions
==================

These functions are used to know when an investment in a PPR generates the same
final tax-net value as a direct investment in the PPR's underlying assets, or with
some defined difference.

In other words, the functions in this section are the result of solving the equation
below for different variables:

.. math::
   PPR \; Tax \text{-} Net \; Value = Underlying \; Assets \; Tax \text{-} Net \; Value + Difference

The functions' pages linked to below contain more details on the calculations made.

.. autosummary::
   :toctree: generated/

   matching_ppr_cost_rate
   matching_ppr_extra_value
   matching_underlying_assets_cagr
