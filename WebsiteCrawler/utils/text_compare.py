import re


class TextCompare:

    def __init__(self, staging_text, production_text):
        self.staging_text = staging_text
        self.production_text = production_text

    def normalize_line(self, line):
        """
        Normalize whitespace only.

        Actual text differences are preserved and detected.
        """

        line = line.strip()

        # Replace multiple spaces/newlines/tabs with one space
        line = re.sub(r"\s+", " ", line)

        return line

    def compare(self):

        # -----------------------------
        # Normalize Staging Text
        # -----------------------------

        staging_lines = [
            self.normalize_line(line)
            for line in self.staging_text.split("\n")
            if line.strip()
        ]

        # -----------------------------
        # Normalize Production Text
        # -----------------------------

        production_lines = [
            self.normalize_line(line)
            for line in self.production_text.split("\n")
            if line.strip()
        ]

        # -----------------------------
        # Exact Line Comparison
        # -----------------------------

        staging_set = set(staging_lines)
        production_set = set(production_lines)

        missing_in_production = staging_set - production_set
        extra_in_production = production_set - staging_set

        differences = []

        # -----------------------------
        # Find Similar Lines
        # -----------------------------

        unmatched_production = set(extra_in_production)

        for staging_line in missing_in_production:

            best_match = None
            best_score = 0

            staging_words = staging_line.lower().split()

            for production_line in unmatched_production:

                production_words = production_line.lower().split()

                if not staging_words or not production_words:
                    continue

                # Compare words without removing duplicates
                common_words = []

                remaining_production_words = production_words.copy()

                for word in staging_words:

                    if word in remaining_production_words:

                        common_words.append(word)
                        remaining_production_words.remove(word)

                score = len(common_words) / max(
                    len(staging_words),
                    len(production_words)
                )

                if score > best_score:

                    best_score = score
                    best_match = production_line

            # -----------------------------
            # Similar Line Found
            # -----------------------------

            if best_match and best_score >= 0.5:

                differences.append({
                    "staging": staging_line,
                    "production": best_match
                })

                unmatched_production.remove(best_match)

            # -----------------------------
            # Staging Line Not Found
            # -----------------------------

            else:

                differences.append({
                    "staging": staging_line,
                    "production": "Not Found"
                })

        # -----------------------------
        # Production-only Lines
        # -----------------------------

        for production_line in unmatched_production:

            differences.append({
                "staging": "Not Found",
                "production": production_line
            })

        # -----------------------------
        # Final Result
        # -----------------------------

        result = "PASS"

        if differences:
            result = "FAIL"

        return {
            "result": result,
            "staging_lines": len(staging_lines),
            "production_lines": len(production_lines),
            "missing_in_production": missing_in_production,
            "extra_in_production": extra_in_production,
            "differences": differences
        }