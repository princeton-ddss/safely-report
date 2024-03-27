# Garbling

Safely Report preserves privacy of survey respondents by recording their responses to
sensitive questions with random noise &mdash; a process known as "garbling".

!!! note

    Garbling works for binary questions only. For instance, the question may ask
    if the respondent experienced any sexual harassment at work, where the possible
    response is either "Yes" or "No".

Specifically, random noise is injected such that

1. Sensitive response (e.g., "Yes" to "Ever harassed sexually?") is always recorded as is
2. The opposite response (e.g., "No" to "Ever harassed sexually?") is *reversed* with the
   pre-specified garbling probability (e.g., 30%)

Mathematically, this can be formulated as follows:

$$
\tilde{r} = r + (1 - r) \cdot \eta
$$

where:

- $r$ is the original binary response between 0 and 1
- $\eta$ is a garbling "shock" that takes the value of either 1 or 0 with the given garbling probability
- $\tilde{r}$ is the garbled response value

The current application supports two types of garbling schemes, which are explained below.

## IID Garbling

Under independent and identically distributed (IID) garbling, whether the given response will be
garbled or not is randomized at the individual level. That is, the value of the garbling shock
(i.e., $\eta \in \{0, 1\}$) is randomly generated for each given response.

## Block Garbling

In contrast, block garbling randomizes garbling shocks at the block/group level. For instance,
with the garbling probability of 40%, block garbling randomly selects and garbles 2 out of
every 5 responses, which works because $2 / 5 = 0.4$.

Note that a "block" can be any group of survey respondents. For instance, it can be
the entire survey population, in which case the randomization is done at the population level
(termed as "population-blocked garbling"). More interestingly, it can be a subgroup of survey
respondents sharing a common attribute such as specific team membership, in which case
the randomization is done at the subgroup level (termed as "covariate-blocked garbling").

Block garbling offers several advantages over IID garbling. First, it enhances privacy assurance
as it ensures that a predetermined proportion (e.g., 40%) of the survey responses are actually garbled,
which in turn guarantees that at least that much proportion has been recorded as sensitive response
(e.g., "Yes" to "Ever harassed sexually?"). This guarantee is especially important if the number of
survey responses is small, in which case IID garbling may fail to garble any response at all.

Another advantage of block garbling is that it improves precision of statistical inference,
especially when underlying reporting rates are low as is often the case for sensitive questions.
Specifically, block garbling reduces variance of an estimate (e.g., mean reporting rates) because
its block-based randomization scheme produces covariance among garbling shocks. For more technical
details, please consult page 17 of this [paper](https://www.nber.org/papers/w31011).

!!! info

    To learn about how to analyze garbling results, check the relevant
    [guide](../guides/analyze-results.md).
