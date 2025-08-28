import logging
from collections import namedtuple
from difflib import SequenceMatcher
from statistics import mean

from refinedoc.enumeration import TargetedPart
from refinedoc.helpers import (
    generate_weights,
    neutralize_arabic_numerals,
    neutralize_roman_numerals,
    unify_list_len,
)

logger = logging.getLogger(__name__)

RefinedDocumentContent = namedtuple(
    "RefinedDocumentContent", ["body", "headers", "footers"]
)


class RefinedDocument:
    def __init__(self, content: list[list[str]], ratio_speed: int = 1, win: int = 8):
        """
        RefinedDocument constructor
        :param content: Document content to be refined
        :param ratio_speed: Speed of the ratio comparison. 1 is the slowest and 3 is the fastest.
        :param win: Window size for header/footer detection. Default is 8.
        """
        if not isinstance(content, list):
            raise TypeError(
                f"RefinedDocument content must be list[list[str]], actual type {type(content)}"
            )

        for i in content:
            if not isinstance(i, list):
                raise TypeError(
                    f"RefinedDocument content must be list[list[str]], actual type {type(i)}"
                )
        if 0 < ratio_speed <= 3:
            self.ratio_speed: int = ratio_speed
            logger.info(f"Ratio speed is fix on {ratio_speed}")
        else:
            raise ValueError(f"Speed must be between 1 and 3: {ratio_speed}")

        self._processed_body: list[list[str]] = content  # Initialize body field
        if len(content) == 1:
            logger.warning(
                "The content provided has only one page. Headers and footers will be set to empty lists."
            )
            self._processed_headers = [[]]
            self._processed_footers = [[]]
        else:
            self._processed_headers: list[list[str]] | None = None
            self._processed_footers: list[list[str]] | None = None

        self.win = win

    @property
    def content(self):
        self._refine_if_required()

        ret = RefinedDocumentContent(
            body=self._processed_body,
            headers=self._processed_headers,
            footers=self._processed_footers,
        )

        return ret

    @property
    def body(self):
        self._refine_if_required()
        return self._processed_body

    @property
    def headers(self):
        self._refine_if_required()
        return self._processed_headers

    @property
    def footers(self):
        self._refine_if_required()
        return self._processed_footers

    def _refine_if_required(self):
        if not self._processed_footers or not self._processed_headers:
            self._separate_header_footer(TargetedPart.HEADER)
            self._separate_header_footer(TargetedPart.FOOTER)

    def _compare(self, from_compare: str, to_compare_candidate: str):
        # Handle page number by replacing it
        from_compare = neutralize_roman_numerals(
            neutralize_arabic_numerals(from_compare)
        ).lower()
        to_compare_candidate = neutralize_roman_numerals(
            neutralize_arabic_numerals(to_compare_candidate)
        ).lower()
        s = SequenceMatcher(None, from_compare, to_compare_candidate)

        if self.ratio_speed == 1:
            ret = s.ratio()
        elif self.ratio_speed == 2:
            ret = s.quick_ratio()
        elif self.ratio_speed == 3:
            ret = s.real_quick_ratio()
        else:
            raise ValueError(f"Speed must be between 1 and 3: {self.ratio_speed}")

        return ret

    def _compare_candidates(
        self, to_compare_candidates: list[str], from_compare: str
    ) -> float:
        computed = [
            self._compare(from_compare, to_compare_candidate)
            for to_compare_candidate in to_compare_candidates
        ]
        ret = mean(computed)
        return ret

    def _detect_similar_lines(
        self,
        candidates: list[str],
        positional_weights: list[float],
        local_neighbours: list[list[str]],
    ) -> list[str]:
        detected = []
        for line_index, candidate in enumerate(candidates):
            try:
                to_compare_candidates = [x[line_index] for x in local_neighbours]
                score = (
                    self._compare_candidates(
                        to_compare_candidates=to_compare_candidates,
                        from_compare=candidate,
                    )
                    * positional_weights[line_index]
                )
            except IndexError as e:
                if line_index >= len(positional_weights):
                    logger.warning(
                        f"Line index {line_index} is out of bounds for positional weights of length {len(positional_weights)}"
                    )
                    score = 0
                else:
                    score = positional_weights[line_index]
            if candidate and score >= 0.5:
                detected.append(candidate)
        return detected

    def _separate_header_footer(
        self, targeted_part: TargetedPart, candidate_quantity: int = 5
    ):

        pages: list[list[str]] = self._processed_body
        header_footer_candidates = []

        for page_content in pages:
            if len(page_content) < candidate_quantity * 2:
                candidate_quantity = len(self._processed_body) // 2
                logger.warning(
                    f"Candidate quantity is too high for the document. Set to {candidate_quantity}"
                )
            if targeted_part == TargetedPart.HEADER:
                header_footer_candidates.append(page_content[:candidate_quantity])
            elif targeted_part == TargetedPart.FOOTER:
                header_footer_candidates.append(page_content[-candidate_quantity:])
            else:
                raise NotImplemented("Value used for targeted part is not usable here")

        identified_headers_footers: list[list[str]] = []

        for page_index, candidates in enumerate(header_footer_candidates):
            down_part = header_footer_candidates[
                max(page_index - self.win, 0) : page_index
            ]
            upper_part = header_footer_candidates[
                min(page_index + 1, len(header_footer_candidates)) : min(
                    page_index + self.win, len(header_footer_candidates)
                )
            ]
            local_neighbours = down_part + upper_part

            if targeted_part == TargetedPart.HEADER:
                unify_list_len(local_neighbours)
            elif targeted_part == TargetedPart.FOOTER:
                unify_list_len(local_neighbours, at_top=True)
            else:
                raise NotImplemented("Value used for targeted part is not usable here")

            standardized_size = len(max(local_neighbours, key=len))
            header_weights = [w for w in generate_weights(standardized_size)]

            if targeted_part == TargetedPart.FOOTER:
                # Inverse weight for footers
                header_weights = header_weights[::-1]

            detected = self._detect_similar_lines(
                candidates=candidates,
                positional_weights=header_weights,
                local_neighbours=local_neighbours,
            )

            pages[page_index] = [x for x in pages[page_index] if x not in detected]
            identified_headers_footers.append(detected)
        self._processed_body = pages

        if targeted_part == TargetedPart.HEADER:
            self._processed_headers = identified_headers_footers
        elif targeted_part == TargetedPart.FOOTER:
            self._processed_footers = identified_headers_footers
        else:
            raise NotImplemented("Value used for targeted part is not usable here")

    def __len__(self) -> int:
        """
        Page quantity in this document
        :return:
        """
        return len(self._processed_body)

    def __getitem__(self, item: int) -> list[str]:
        """
        Get page content
        :param item: page index
        :return: page content
        """
        return self._processed_body[item]
