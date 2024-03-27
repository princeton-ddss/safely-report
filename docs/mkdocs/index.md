# What is Safely Report?

Survey participants often feel reluctant to share their true experience because they are worried about
potential retaliation in case their responses are identified (e.g., data leakage). This is especially
the case for sensitive survey questions such as those asking about sexual harassment in the workplace.
As a result, survey administrators (e.g., company management, researchers) often get inaccurate
representation of the reality, which makes it hard to devise an appropriate course of action.

Safely Report is a survey web application that can provide plausible deniability to survey respondents
by recording survey responses with noise. For instance, when asking a worker whether they have been harassed
by a manager, the application can be set up to record the answer "yes" with a probability of 30% even if
the worker responds "no". This makes it nearly impossible to correctly identify which responses (of all those
recorded "yes") are truthful reports &mdash; even if the survey results are leaked. Yet, the survey designer
can still well estimate the *proportion* and other statistics of truthful reports because they know the rate
of noise injection. Consequently, survey participants feel more safe and become more willing to share their
true experience, which has been confirmed by a relevant [study](https://www.nber.org/papers/w31011).

!!! tip "Sounds interesting?"

    Read about [concepts](concepts/garbling.md) behind Safely Report.
    Or, check out the [quickstart](quickstart.md) guide to try out the application.
