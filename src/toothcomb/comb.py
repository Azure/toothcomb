"""Utilities for combing logs for interesting entries."""
import logging
import re

LOGGER = logging.getLogger(__name__)


def count_report(count_dict):
    """
    Return report from dictionary of counts.

    :param count_dict:
    """
    # sort by descending count, increasing label
    report = ""
    for (label, count) in sorted(count_dict.items(), key=lambda x: (-x[1], x[0])):
        if count:
            report += "{}: {}\n".format(label, count)
    return report


def match_spec(text, spec):
    """
    Match text against keyed re spec.

    :param text: text to check
    :param spec: comb spec {"label": [re]}
    :return: matched key or None
    """
    for (label, re_list) in spec.items():
        for regex in re_list:
            if regex.search(text):
                return label
    return None


def match_counts(blocks, spec):
    """
    Return dictionary of match counts.

    :param blocks: list of blocks of text to check
    :param spec: comb spec {"label": [re]}
    :return: {"label": count}
    """
    matched_counts = {}
    for label in spec.keys():
        matched_counts[label] = 0
    for block in blocks:
        matched_label = match_spec(block, spec)
        if matched_label:
            matched_counts[matched_label] += 1
    return matched_counts


def unmatched_blocks(blocks, spec):
    """
    Return list of unmatched blocks.

    :param blocks: list of blocks of text to check
    :param spec: comb spec {"label": [re]}
    :return: list of unmatched blocks
    """
    unmatched = []
    for block in blocks:
        if block and not match_spec(block, spec):
            unmatched.append(block)
    return unmatched


class Toothcomb:
    """Toothcomb."""

    def __init__(self, spec, text):
        """
        Initialise.

        :param spec: comb specification dictionary
        :param text: text to be analysed
        """
        self._explained = {}
        self._livewith = {}
        self._monitor = {}
        for live_spec in spec.get("livewith"):
            label = live_spec.get("label", "other")
            if label not in self._livewith.keys():
                self._livewith[label] = []
            if label not in self._explained.keys():
                self._explained[label] = []
            for exp in live_spec.get("regexp", []):
                self._livewith[label].append(re.compile(exp))
                self._explained[label].append(re.compile(exp))
        for monitor_spec in spec.get("monitor"):
            label = monitor_spec.get("label", "other")
            if label not in self._monitor.keys():
                self._monitor[label] = []
            if label not in self._explained.keys():
                self._explained[label] = []
            for exp in monitor_spec.get("regexp", []):
                self._monitor[label].append(re.compile(exp))
                self._explained[label].append(re.compile(exp))
        self._blocksplit = spec.get("blocksplit", "\n")
        self._blocks = text.split(self._blocksplit)

    def annotated_text(self):
        """
        Return annotated text report.

        :return: annotated text report
        """
        if self._blocksplit == "\n":
            monitor_annotation = "M "
            livewith_annotation = "L "
            unmatched_annotation = "  "
        else:
            monitor_annotation = "\nmonitor\n"
            livewith_annotation = "\nlivewith\n"
            unmatched_annotation = "\nunexplained\n"
        report = ""
        for block in self._blocks:
            annotation = unmatched_annotation
            if match_spec(block, self._monitor):
                annotation = monitor_annotation
            elif match_spec(block, self._livewith):
                annotation = livewith_annotation
            report += "{}{}{}".format(self._blocksplit, annotation, block)
        return report

    def livewith_report(self):
        """
        Return livewith report.

        :return: livewith report
        """
        report = ""
        report += "livewith\n"
        report += "========\n"
        return report + count_report(match_counts(self._blocks, self._livewith))

    def monitor_report(self):
        """
        Return monitor report.

        :return: monitorlivewith report
        """
        report = ""
        report += "monitor\n"
        report += "=======\n"
        return report + count_report(match_counts(self._blocks, self._monitor))

    def unexplained_report(self):
        """
        Return unexplained report.

        :return: unexplained report
        """
        report = ""
        unmatched = unmatched_blocks(self._blocks, self._explained)
        if unmatched:
            report += "unexplained\n"
            report += "===========\n"
            report += self._blocksplit.join(
                unmatched_blocks(self._blocks, self._explained)
            )
        return report
