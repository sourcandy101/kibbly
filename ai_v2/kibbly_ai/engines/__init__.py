"""Engines: deterministic code for every number and decision.

Nutrition and feeding plan (step 5), meal statistics, daily summaries, anomaly
flags and alert rules (step 6), dispensing rules (step 7). Fully unit tested,
no model inside.
"""

from kibbly_ai.engines.nutrition import FeedingPlan, Meal, age_in_months, feeding_plan
from kibbly_ai.engines.serving import Decision, decide

__all__ = ["Decision", "decide", "FeedingPlan", "Meal", "age_in_months", "feeding_plan"]
