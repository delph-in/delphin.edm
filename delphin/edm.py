
"""
Elementary Dependency Matching
"""

from typing import Union, List, Tuple, Iterable, Any
import logging
from collections import Counter
from itertools import zip_longest

from delphin.lnk import LnkMixin
from delphin.eds import EDS
from delphin.dmrs import DMRS

__version__ = '0.1.0'


logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


_SemanticRepresentation = Union[EDS, DMRS]
_Span = Tuple[int, int]
_Triple = Tuple[_Span, str, Any]
_Counts = Tuple[int, int, int]
_AllCounts = Tuple[_Counts, _Counts, _Counts, _Counts]
_Scores = Tuple[float, float, float]


def span(node: LnkMixin) -> _Span:
    """Return the Lnk span of a Node as a (cfrom, cto) tuple."""
    return (node.cfrom, node.cto)


def names(sr: _SemanticRepresentation) -> List[_Triple]:
    """Return the list of name (predicate) triples for *sr*."""
    triples = []
    for node in sr.nodes:
        triples.append((span(node), node.predicate))
    return triples


def arguments(sr: _SemanticRepresentation) -> List[_Triple]:
    """Return the list of argument triples for *sr*."""
    triples = []
    args = sr.arguments()
    for node in sr.nodes:
        source_span = span(node)
        for role, target in args[node.id]:
            if target in sr:
                triples.append((source_span, role, span(sr[target])))
    return triples


def properties(sr: _SemanticRepresentation) -> List[_Triple]:
    """Return the list of property triples for *sr*."""
    triples = []
    for node in sr.nodes:
        node_span = span(node)
        for feature, value in node.properties.items():
            triples.append((node_span, feature, value))
        if node.carg:
            triples.append((node_span, 'carg', node.carg))
    return triples


def match(gold: _SemanticRepresentation,
          test: _SemanticRepresentation) -> _AllCounts:
    """
    Return the counts of triples for *gold* and *test*.

    The counts are a list of lists of counts as follows::

        # gold test both
        [[gn,  tn,  bn],  # name counts
         [ga,  ta,  ba],  # argument counts
         [gp,  tp,  bp],  # property counts
         [gt,  tt,  bt]]  # top counts
    """
    counts = []
    for func in names, arguments, properties:
        gold_triples = func(gold)
        test_triples = func(test)
        c1 = Counter(gold_triples)
        c2 = Counter(test_triples)
        both = sum(min(c1[t], c2[t]) for t in c1 if t in c2)
        counts.append((len(gold_triples), len(test_triples), both))

    gold_top = 1 if gold.top in gold else 0
    test_top = 1 if test.top in test else 0
    if gold_top and test_top and span(gold[gold.top]) == span(test[test.top]):
        both_top = 1
    else:
        both_top = 0
    counts.append((gold_top, test_top, both_top))

    return counts


def compute(golds: Iterable[_SemanticRepresentation],
            tests: Iterable[_SemanticRepresentation],
            name_weight: float = 1.0,
            argument_weight: float = 1.0,
            property_weight: float = 1.0,
            top_weight: float = 1.0) -> _Scores:
    debug = logger.isEnabledFor(logging.DEBUG)
    logger.info('Computing EDM (N=%g, A=%g, P=%g, T=%g)',
                name_weight, argument_weight, property_weight, top_weight)

    totals = ((0, 0, 0),  # name (predicate) (gold, test, both)
              (0, 0, 0),  # argument         (gold, test, both)
              (0, 0, 0),  # property         (gold, test, both)
              (0, 0, 0))  # top              (gold, test, both)

    for i, (gold, test) in enumerate(zip_longest(golds, tests), 1):
        if gold is None:
            logger.error('more test items than gold items; ignoring the rest')
            break
        if test is None:
            logger.error('more gold items than test items; ignoring the rest')
            break

        logger.info('comparing pair %d', i)
        counts = match(gold, test)

        if debug:
            logger.debug(
                '             gold\ttest\tboth\tPrec.\tRec.\tF-Score')
            fmt = '%11s: %4d\t%4d\t%4d\t%5.3f\t%5.3f\t%5.3f'
            logger.debug(fmt, 'Names', *counts[0], *_prf(*counts[0]))
            logger.debug(fmt, 'Arguments', *counts[1], *_prf(*counts[1]))
            logger.debug(fmt, 'Properties', *counts[2], *_prf(*counts[2]))
            logger.debug(fmt, 'Tops', *counts[3], *_prf(*counts[3]))

        totals = tuple(
            [(tot[0] + cnt[0],
              tot[1] + cnt[1],
              tot[2] + cnt[2])
             for tot, cnt in zip(totals, counts)])

    gold_total = (totals[0][0] * name_weight
                  + totals[1][0] * argument_weight
                  + totals[2][0] * property_weight
                  + totals[3][0] * top_weight)
    test_total = (totals[0][1] * name_weight
                  + totals[1][1] * argument_weight
                  + totals[2][1] * property_weight
                  + totals[3][1] * top_weight)
    both_total = (totals[0][2] * name_weight
                  + totals[1][2] * argument_weight
                  + totals[2][2] * property_weight
                  + totals[3][2] * top_weight)

    return _prf(gold_total, test_total, both_total)


def _prf(g, t, b):
    if t == 0 or g == 0 or b == 0:
        return 0, 0, 0
    else:
        p = b / t
        r = b / g
        f = 2 * (p * r) / (p + r)
        return p, r, f
