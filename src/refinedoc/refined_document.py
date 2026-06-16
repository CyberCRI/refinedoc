import logging
from collections import namedtuple
from difflib import SequenceMatcher
from statistics import mean

from refinedoc.enumeration import TargetedPart
from refinedoc.helpers import (
    generate_weights,
    neutralize_arabic_numerals,
    neutralize_roman_numerals,
)

logger = logging.getLogger(__name__)
UNSUPPORTED_TARGETED_PART_MSG = "Value used for targeted part is not usable here"

RefinedDocumentContent = namedtuple(
    "RefinedDocumentContent", ["body", "headers", "footers"]
)


class RefinedDocument:
    """Represent a paginated document with extracted headers and footers."""

    def __init__(self, content: list[list[str]], ratio_speed: int = 1, win: int = 8):
        """
        Initialize a document and configure comparison behavior.

        :param content: Document content, organized as ``list[page_lines]``.
        :type content: list[list[str]]
        :param ratio_speed: Similarity mode (1=accurate, 3=fastest).
        :type ratio_speed: int
        :param win: Number of neighboring pages used for local comparison.
        :type win: int
        :raises TypeError: If ``content`` is not a ``list[list[str]]`` structure.
        :raises ValueError: If ``ratio_speed`` is not in ``[1, 3]``.
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
    def content(self) -> RefinedDocumentContent:
        """Return processed body, headers, and footers.

        :return: Container with refined content parts.
        :rtype: RefinedDocumentContent
        """
        self._refine_if_required()

        ret = RefinedDocumentContent(
            body=self._processed_body,
            headers=self._processed_headers,
            footers=self._processed_footers,
        )

        return ret

    @property
    def body(self) -> list[list[str]]:
        """Return document body without detected headers and footers.

        :return: Refined page contents.
        :rtype: list[list[str]]
        """
        self._refine_if_required()
        return self._processed_body

    @property
    def headers(self) -> list[list[str]] | None:
        """Return detected headers for each page.

        :return: Header lines grouped by page.
        :rtype: list[list[str]] | None
        """
        self._refine_if_required()
        return self._processed_headers

    @property
    def footers(self) -> list[list[str]] | None:
        """Return detected footers for each page.

        :return: Footer lines grouped by page.
        :rtype: list[list[str]] | None
        """
        self._refine_if_required()
        return self._processed_footers

    def _refine_if_required(self) -> None:
        """Run extraction lazily if headers/footers are not already computed.

        :return: ``None``.
        :rtype: None
        """
        if not self._processed_footers or not self._processed_headers:
            self._separate_header_footer(TargetedPart.HEADER)
            self._separate_header_footer(TargetedPart.FOOTER)

    def _compare(self, from_compare: str, to_compare_candidate: str) -> float:
        """Compare two lines after neutralizing page-number-like tokens.

        :param from_compare: Reference text.
        :type from_compare: str
        :param to_compare_candidate: Candidate text to compare.
        :type to_compare_candidate: str
        :return: Similarity score between 0 and 1.
        :rtype: float
        :raises ValueError: If ``ratio_speed`` is outside supported values.
        """
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
        """Compute mean similarity between one line and multiple candidates.

        :param to_compare_candidates: Lines from neighboring pages.
        :type to_compare_candidates: list[str]
        :param from_compare: Line from the current page.
        :type from_compare: str
        :return: Mean similarity score.
        :rtype: float
        """
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
        """Detect candidate lines that are similar across neighboring pages.

        :param candidates: Candidate lines from one page.
        :type candidates: list[str]
        :param positional_weights: Positional confidence weights.
        :type positional_weights: list[float]
        :param local_neighbours: Candidate lines from surrounding pages.
        :type local_neighbours: list[list[str]]
        :return: Lines considered as header/footer content.
        :rtype: list[str]
        """
        detected = []
        for line_index, candidate in enumerate(candidates):
            if line_index >= len(positional_weights):
                logger.warning(
                    f"Line index {line_index} is out of bounds for positional weights of length {len(positional_weights)}"
                )
                score = 0
            else:
                # Compare only with neighbors that actually contain this line index.
                to_compare_candidates = [
                    x[line_index] for x in local_neighbours if line_index < len(x)
                ]
                if not to_compare_candidates:
                    score = 0
                else:
                    score = (
                        self._compare_candidates(
                            to_compare_candidates=to_compare_candidates,
                            from_compare=candidate,
                        )
                        * positional_weights[line_index]
                    )
            if candidate and score >= 0.5:
                detected.append(candidate)
        return detected

    def _separate_header_footer(
        self, targeted_part: TargetedPart, candidate_quantity: int = 5
    ) -> None:
        """Extract and remove either headers or footers from page contents.

        :param targeted_part: Area to process (header or footer).
        :type targeted_part: TargetedPart
        :param candidate_quantity: Number of candidate lines per page.
        :type candidate_quantity: int
        :return: ``None``.
        :rtype: None
        :raises NotImplementedError: If ``targeted_part`` is unsupported.
        """

        header_footer_candidates = self._identify_candidates(
            candidate_quantity, targeted_part
        )

        identified_headers_footers: list[list[str]] = []
        pages = self._processed_body.copy()

        for page_index, candidates in enumerate(header_footer_candidates):
            local_neighbours = self._identify_local_neighbours(
                header_footer_candidates, page_index
            )

            # Align neighbor lengths so each index represents the same relative line.
            if not local_neighbours:
                identified_headers_footers.append([])
                continue

            standardized_size = max(
                len(candidates), len(max(local_neighbours, key=len, default=[]))
            )

            # Pad neighbors to the same size as the local comparison window.
            self._pad_neighbours(local_neighbours, standardized_size, targeted_part)

            header_weights = list(generate_weights(standardized_size))

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
            raise NotImplementedError(UNSUPPORTED_TARGETED_PART_MSG)

    @staticmethod
    def _pad_neighbours(
        local_neighbours: list[list[str]],
        standardized_size: int,
        targeted_part: TargetedPart,
    ):
        for neighbour in local_neighbours:
            deficit = standardized_size - len(neighbour)
            if deficit <= 0:
                continue
            if targeted_part == TargetedPart.FOOTER:
                neighbour[:0] = [""] * deficit
            else:
                neighbour.extend([""] * deficit)

    def _identify_local_neighbours(
        self, header_footer_candidates: list[list[str]], page_index: int
    ) -> list[list[str]]:
        """
        Identify neighboring pages for local comparison.

        :param header_footer_candidates: List of candidate lines to extract.
        :param page_index: Page index for which to find neighbors.
        :return: List of neighboring candidate lines.
        :rtype: list[list[str]]
        """
        down_part = header_footer_candidates[max(page_index - self.win, 0) : page_index]
        upper_part = header_footer_candidates[
            min(page_index + 1, len(header_footer_candidates)) : min(
                page_index + self.win, len(header_footer_candidates)
            )
        ]
        local_neighbours = down_part + upper_part
        return local_neighbours

    def _identify_candidates(
        self, candidate_quantity: int, targeted_part: TargetedPart
    ) -> list[list[str]]:
        """Collect header/footer candidate lines for each page.

        :param candidate_quantity: Number of lines to keep from top/bottom.
        :type candidate_quantity: int
        :param targeted_part: Area to inspect (header or footer).
        :type targeted_part: TargetedPart
        :return: Candidate lines for each page.
        :rtype: list[list[str]]
        :raises NotImplementedError: If ``targeted_part`` is unsupported.
        """
        header_footer_candidates = []

        for page_content in self._processed_body:
            effective_candidate_quantity = candidate_quantity
            if len(page_content) < effective_candidate_quantity * 2:
                effective_candidate_quantity = (
                    (len(page_content) + 1) // 2 if page_content else 0
                )
                logger.warning(
                    f"Candidate quantity is too high for the document. Set to {effective_candidate_quantity}"
                )

            if effective_candidate_quantity == 0:
                logger.warning("A page is empty, no header or footer can be identified")
                header_footer_candidates.append([])
                continue

            if targeted_part == TargetedPart.HEADER:
                header_footer_candidates.append(
                    page_content[:effective_candidate_quantity]
                )
            elif targeted_part == TargetedPart.FOOTER:
                header_footer_candidates.append(
                    page_content[-effective_candidate_quantity:]
                )
            else:
                raise NotImplementedError(UNSUPPORTED_TARGETED_PART_MSG)
        return header_footer_candidates

    def __len__(self) -> int:
        """
        Return the number of pages in the document.

        :return: Page count.
        :rtype: int
        """
        return len(self._processed_body)

    def __getitem__(self, item: int) -> list[str]:
        """
        Return page content by index.

        :param item: Page index.
        :type item: int
        :return: Lines of the selected page.
        :rtype: list[str]
        """
        return self._processed_body[item]
