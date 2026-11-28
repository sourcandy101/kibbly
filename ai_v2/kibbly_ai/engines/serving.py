"""Serving decision: turn a recognition result into what the feeder should do.

Perception answers who is there (perception/recognizer.py). The decision to dispense
is a rule and lives here, in the engines, so it is deterministic and unit tested.
The ESP32-CAM forwards the action to the STM32, which does the dispensing.
"""

from dataclasses import dataclass

# Actions the STM32 understands. Keep these strings stable: the firmware switches on them.
SERVE = "serve"                      # the dog whose meal it is: dispense in bursts while it stays
BLOCK = "block"                      # a known dog, but not this meal's dog: dispense nothing
UNKNOWN_PORTION = "unknown_portion"  # an unknown dog: a small portion and notify the owner with a photo
WAIT = "wait"                        # unsure between two dogs: dispense nothing, check again shortly
NOTHING = "nothing"                  # no dog (a person, or an empty view): do nothing


@dataclass(frozen=True)
class Decision:
    action: str
    allow_dispense: bool   # may the STM32 release food at all
    reason: str


def decide(result, meal_dog: str = None) -> Decision:
    """Decide from a RecognitionResult.

    meal_dog is the dog whose meal is being served, from the calling order. When it is None
    (a check outside a meal) a known dog gets BLOCK: nothing is dispensed without a meal.
    """
    if result.classification == "not_a_dog":
        return Decision(NOTHING, False, "no dog in view")

    if result.classification == "unknown_dog":
        if "unsure" in (result.reason or ""):
            return Decision(WAIT, False, "unsure between two dogs, check again")
        return Decision(UNKNOWN_PORTION, True, "unknown dog, small portion and notify the owner")

    # known_dog
    if meal_dog is None:
        return Decision(BLOCK, False, f"{result.dog_id} recognized, but no meal is being served")
    if result.dog_id == meal_dog:
        return Decision(SERVE, True, f"{result.dog_id} is this meal's dog")
    return Decision(BLOCK, False, f"{result.dog_id} is not this meal's dog ({meal_dog})")
