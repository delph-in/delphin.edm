# delphin.edm

Elementary Dependency Matching ([EDM][]; [Dridan and Oepen, 2011][])
is a metric for comparing two semantic dependency graphs that annotate
the same sentence. It requires that each node is aligned to a
character span in the original sentence.

The newer [smatch][] metric is essentially the same except that
instead of relying on surface-aligned nodes it finds a mapping of
nodes that optimizes the number of matching triples. The search uses
stochastic hill-climbing, whereas EDM gives deterministic results.

## Installation and Requirements

This module works with Python 3.6 and higher, and it is a [namespace
package][] of [PyDelphin][].

This module can be installed via `pip`:

``` console
$ git clone https://github.com/delph-in/delphin.edm.git
$ pip install delphin.edm/
```

## Usage

Once installed, `edm` is a subcommand of PyDelphin's `delphin`
command. The basic usage is:

``` console
$ delphin edm GOLD TEST
```

For example:

``` console
$ delphin edm test/kim.gold.eds test/kim.test.eds
Precision:	0.9344262295081968
   Recall:	0.9193548387096774
  F-score:	0.9268292682926829
```

Per-item information can be printed by increasing the logging
verbosity to the `INFO` level (`-vv`). Weights for the different
classes of triples can be adjusted with `-A`, `-N`, `-P`, and
`-T`. Try `delphin edm --help` for more information.

This implementation can read semantic representations in a [variety of
formats][codecs] via the `--format` option, and it can also read from
[[incr tsdb()]][itsdb] databases. It can compute EDM for Elementary
Dependency Structures (EDS), Dependency Minimal Recursion Semantics
(DMRS), and Minimal Recursion Semantics (MRS). For MRS,
representations are first converted into EDS.

## Differences from Dridan and Oepen, 2011

Following the [mtool][] implementation, I treat constant arguments
(`CARG`) as a property ("class 3 information" in [Dridan and Oepen,
2011][]). I also follow [mtool][] in checking if the graph tops are
the same.

This implementation is unique in that it allows for weighting the
different classes of information instead of just disabling/enabling
them.

## Other Implementations

* Rebecca Dridan's original Perl version (see
  http://moin.delph-in.net/ElementaryDependencyMatch)
* [mtool][]
* As part of [[incr tsdb()]][itsdb]
* As part of [DeepDeepParser][]

[smatch]: https://github.com/snowblink14/smatch/
[namespace package]: https://docs.python.org/3/reference/import.html#namespace-packages
[EDM]: http://moin.delph-in.net/ElementaryDependencyMatch
[Dridan and Oepen, 2011]: https://www.aclweb.org/anthology/W11-2927/
[PyDelphin]: https://github.com/delph-in/pydelphin
[codecs]: https://pydelphin.readthedocs.io/en/v1.0.0/api/delphin.codecs.html
[itsdb]: http://moin.delph-in.net/ItsdbTop
[mtool]: https://github.com/cfmrp/mtool
[DeepDeepParser]: https://github.com/janmbuys/DeepDeepParser
