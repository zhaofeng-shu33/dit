"""
Utilities related to testing.
"""

from __future__ import division

from hypothesis import assume
from hypothesis.strategies import composite, floats, integers, lists, tuples

from .. import Distribution

@composite
def distributions(draw, size=(3, 4), alphabet=(2, 4), uniform=False, min_events=1):
    """
    A hypothesis strategy for generating distributions.

    Parameters
    ----------
    draw : function
        A sampling function passed in by hypothesis.
    size : int
        The size of outcomes desired. Defaults to a 3 or 4, randomly.
    alphabet : int
        The alphabet size for each variable. Defaults to 2, 3, or 4, randomly.
    uniform : bool
        Whether the probabilities should be uniform or random. Defaults to random.

    Returns
    -------
    dist : Distribution
        A random distribution.
    """
    try:
        len(size)
    except TypeError:
        size = (size, size)
    try:
        len(alphabet)
    except TypeError:
        alphabet = (alphabet, alphabet)

    size_ = draw(integers(*size))
    alphabet_ = draw(integers(*alphabet))

    events = draw(lists(tuples(*[integers(0, alphabet_ - 1)] * size_), min_size=min_events, unique=True))

    if uniform:
        probs = [1 / len(events)] * len(events)
    else:
        probs = draw(tuples(*[floats(0, 1)] * len(events)))
        for prob in probs:
            assume(prob > 0)
        total = sum(probs)
        probs = [p / total for p in probs]

    return Distribution(events, probs)
