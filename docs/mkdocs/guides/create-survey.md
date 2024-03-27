# Creating Survey Files

Three files are required to run Safely Report:

| File                | Description                                                        |
| ------------------- | ------------------------------------------------------------------ |
| XLSForm             | An Excel file specifying survey questions and other metadata       |
| Respondent Roster   | A CSV file listing respondents and their attributes (e.g., name)   |
| Enumerator Roster   | A CSV file listing enumerators and their attributes (e.g., name)   |

## XLSForm

### XLSForm Basics

If you are not familiar with XLSForm, please check out the following video tutorials:[^1]

1. [Form Structure](https://youtu.be/V_IAzwoXwyk?si=rgQwu_OmybwzhRPH)
2. [Question Types](https://youtu.be/YSTaKmtkFBw?si=NvYKJCYPLLVeEvby)
3. [Question Types: Examples](https://youtu.be/92Tyurcntwg?si=GmmunmD8U5wTHdZ9)
4. [Form Logic](https://youtu.be/d8q0XtxT0Uk?si=AacqbrjU5jEYDB_P)
5. [Form Logic: Examples](https://youtu.be/91G8z0ggOBM?si=UaHaLrs627tBsa7D)

To learn more about XLSForm, please check out this [reference](https://docs.getodk.org/xlsform/) by ODK.

### Validating XLSForm

You can use this [tool](https://getodk.org/xlsform/) to validate and preview your XLSForm.

Please note that Safely Report validates XLSForm for additional requirements including:

- No infinite repeats (1)
    { .annotate }

    1.  Instead, the survey can be designed to have the respondent dynamically set and change
        the number of repeats. For instance, if the survey has a repeat section asking details
        of family members (e.g., name, age), it can first ask how many family members
        the respondent has and then, based on this response, perform repeats.

- No nested repeats (1)
    { .annotate }

    1.  Nested repeats introduce unnecessary complication to administration of the survey itself.

!!! note

    Safely Report may not support all XLSForm functions and question types.
    If you need to use a specific function or question type that is currently unavailable,
    please submit a request following the process [here](get-help.md).

### Specifying Garbling

!!! info

    If you are not familiar with garbling, please review relevant concepts [here](../concepts/garbling.md).

Garbling parameters can be specified in the `survey` sheet of XLSForm, specifically in the following columns:

- `garbling::answer`
    - Name (not label) of the choice option to be garbled into.
    - Most of the time, it is the name of the "yes" choice option.

- `garbling::rate`
    - Rate at which garbling will be applied.
    - For block garbling, supported rates are limited to the following values:

        | Rate   | Description                               |
        | ------ | ----------------------------------------- |
        | `0.20` | For every 5 responses, garble 1 of them   |
        | `0.25` | For every 4 responses, garble 1 of them   |
        | `0.40` | For every 5 responses, garble 2 of them   |
        | `0.50` | For every 2 responses, garble 1 of them   |
        | `0.60` | For every 5 responses, garble 3 of them   |
        | `0.75` | For every 4 responses, garble 3 of them   |
        | `0.80` | For every 5 responses, garble 4 of them   |

- `garbling::covariate`
    - Name of a covariate to use for covariate-blocked garbling.
    - If asterisk (`*`), it performs population-blocked garbling.
    - If unspecified, it performs IID garbling.

Please note that garbling cannot be applied inside a repeat section because this makes it
impossible to control the number of garbling performed under block garbling.

For a working example/reference, you can check this
[file](https://github.com/princeton-ddss/safely-report/raw/dev/tests/data/stats4sd_example_xlsform_adapted.xlsx).

## Rosters

Rosters should be provided as CSV files that can contain any columns and data.

Note that the respondent roster should include all covariates to be used for block garbling.
That is, covariate values for block garbling cannot be gathered from the survey;
they need to exist in the roster.

!!! warning

    `id` is a reserved name for system-generated IDs, so an error will be raised
    if a roster contains a column by this name.

[^1]: Produced by [Statistics for Sustainable Development (Stats4SD)](https://stats4sd.org/collections/29)
