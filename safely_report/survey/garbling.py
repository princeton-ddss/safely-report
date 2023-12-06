from dataclasses import dataclass
from enum import Enum
from random import random
from typing import Any, Optional

from flask_sqlalchemy import SQLAlchemy
from pyxform.xls2json import parse_file_to_json

from safely_report.survey.survey_session import SurveySession
from safely_report.utils import check_dict_required_fields


class GarblingScheme(Enum):
    IID = "Independent and Identically Distributed"
    PopBlock = "Population-Blocked"
    CovBlock = "Covariate-Blocked"


@dataclass(frozen=True)
class GarblingParams:
    # Name of the survey element to be garbled
    question: str

    # Name (not label) of the choice option to be garbled *into*
    # Most of the time, it is the name of the "yes" choice option
    answer: str

    # Garbling probability
    rate: float

    # Name of a covariate to use for Covariate-Blocked Garbling
    covariate: Optional[str]

    @property
    def scheme(self) -> GarblingScheme:
        if not self.covariate:
            return GarblingScheme.IID
        elif self.covariate == "*":
            return GarblingScheme.PopBlock
        else:
            return GarblingScheme.CovBlock


class Garbler:
    """
    A garbling engine that parses garbling specifications in XLSForm
    and uses them to perform different garbling schemes.

    Parameters
    ----------
    path_to_xlsform: str
        Path to the XLSForm file specifying the survey
    session: SurveySession
        Session object for caching data specific to current survey respondent
    db: SQLAlchemy
        An instance of database connection
    """

    def __init__(
        self, path_to_xlsform: str, session: SurveySession, db: SQLAlchemy
    ):
        self._params = self._parse_xlsform(path_to_xlsform)
        self._session = session
        self._db = db

        # TODO: Cache covariate info of current survey respondent
        # (create and use related methods in SurveySession)
        pass

    def get_garbling_params(
        self, survey_element_name: str
    ) -> Optional[GarblingParams]:
        """
        Retrieve garbling parameters of the given survey element.
        Return `None` if the given survey element is not subject to garbling.

        Parameters
        ----------
        survey_element_name: str
            Name of the survey element to be garbled

        Returns
        -------
        GarblingParams, optional
            Garbling parameters of the given survey element
        """
        return self._params.get(survey_element_name)

    def get_garbling_shock(self, garbling_params: GarblingParams) -> bool:
        if garbling_params.scheme == GarblingScheme.IID:
            # Randomize garbling shock at the individual level
            garbling_shock = True if random() < garbling_params.rate else False

            # TODO: Cache it in session for potential later reuse
            pass
        elif garbling_params.scheme == GarblingScheme.PopBlock:
            # TODO: Try using cached data (if existing)
            pass

            # TODO: If cached data is not available, pull it from DB
            # (and cache it in session for potential later reuse)
            pass

        return garbling_shock

    @staticmethod
    def _parse_xlsform(path_to_xlsform: str) -> dict[str, GarblingParams]:
        """
        Parse XLSForm to identify questions subject to garbling
        and their respective parameters.

        Parameters
        ----------
        path_to_xlsform: str
            Path to the XLSForm file specifying the survey

        Returns
        -------
        dict[str, GarblingParams]
            Dictionary that maps garbling parameters onto
            the corresponding target question name
        """
        survey_dict = parse_file_to_json(path=path_to_xlsform)

        # Recursively identify survey elements subject to garbling
        # NOTE: Ensure no garbling happens inside any repeat section
        a = Garbler._find_elements_with_garbling(survey_dict)
        b = Garbler._find_elements_with_garbling(survey_dict, skip_repeat=True)
        if len(a) > len(b):
            raise Exception("Garbling should not be applied inside repeats")
        elements_with_garbling = b

        # Extract and organize garbling parameters
        garbling_params = {}
        for element in elements_with_garbling:
            name = element.get("name", "")
            garbling_params[name] = Garbler._extract_garbling_params(element)

        return garbling_params

    @staticmethod
    def _find_elements_with_garbling(
        element: dict[str, Any],
        skip_repeat: bool = False,
        elements_with_garbling: Optional[list[dict[str, Any]]] = None,
    ) -> list[dict[str, Any]]:
        """
        Recursively identify survey elements subject to garbling.

        Parameters
        ----------
        element: dict[str, Any]
            A record in the dictionary representation of the survey
            produced by `pyxform.xls2json.parse_file_to_json()`
        skip_repeat: bool
            Whether to discard survey elements under repeat sections
        elements_with_garbling: list[dict[str, Any]], optional
            Existing array of survey elements subject to garbling

        Returns
        -------
        list[dict[str, Any]]
            Array of survey elements subject to garbling
        """
        if elements_with_garbling is None:
            elements_with_garbling = []

        # Determine whether the given survey element is a repeat section
        is_repeat = element.get("type") == "repeat"

        # Recursively identify survey elements subject to garbling
        if not skip_repeat or (skip_repeat and not is_repeat):
            if element.get("garbling"):
                elements_with_garbling.append(element)
            if element.get("children"):
                for child in element["children"]:
                    Garbler._find_elements_with_garbling(
                        element=child,
                        skip_repeat=skip_repeat,
                        elements_with_garbling=elements_with_garbling,
                    )

        return elements_with_garbling

    @staticmethod
    def _extract_garbling_params(element: dict[str, Any]) -> GarblingParams:
        """
        Extract, validate, and repackage garbling parameters
        for the given survey element record.

        Parameters
        ----------
        element: dict[str, Any]
            A record in the dictionary representation of the survey
            produced by `pyxform.xls2json.parse_file_to_json()`

        Returns
        -------
        GarblingParams
            Streamlined packaging of validated garbling parameters
        """
        # Unpack the given survey record
        check_dict_required_fields(
            data=element,
            required_fields=[
                ("name", str),
                ("choices", list),
                ("garbling", dict),
            ],
        )
        params = element["garbling"]
        question = element["name"]
        choices = element["choices"]

        # Unpack garbling parameters
        check_dict_required_fields(
            data=params,
            required_fields=[("answer", str), ("rate", str)],
        )
        answer = params["answer"]
        rate = float(params["rate"])
        covariate = params.get("covariate")  # Optional param

        # Validate garbling parameters
        if len(choices) != 2:
            raise Exception(
                "Garbling specified for a non binary-choice question: "
                f"{question}"
            )
        choice_names = [c.get("name", "") for c in choices]
        if answer not in choice_names:
            raise Exception(f"{answer} not in choice options for {question}")
        if rate < 0 or rate > 1:
            raise Exception("Garbling rate should be between 0 and 1")

        return GarblingParams(question, answer, rate, covariate)

    @staticmethod
    def _garble_response(
        garbling_answer: str,
        garbling_shock: bool,
        response_value: str,
    ) -> str:
        """
        Apply garbling formula to the given response.

        With binary response between 0 and 1, garbling is formally defined as:

            r_tilde = r + (1 - r) * eta

        where:

            - `r` is the original raw response value
            - `eta` is a garbling "shock" that takes the value of either 1 or 0
            with the given garbling probability
            - `r_tilde` is the garbled response value

        For more details, consult the original paper:

            https://www.nber.org/papers/w31011

        Parameters
        ----------
        garbling_answer: str
            Name (not label) of the choice option to be garbled *into*
            (most of the time, it is the name of the "yes" choice option)
        garbling_shock: bool
            Garbling "shock" that takes the value of either 1 or 0
            with the given garbling probability
        response_value: str
            Name (not label) of the choice option that the respondent selected

        Returns
        -------
        str
            Name (not label) of the choice option after garbling is applied
        """
        if response_value == garbling_answer:
            return response_value
        else:
            if garbling_shock is True:
                return garbling_answer
            else:
                return response_value
