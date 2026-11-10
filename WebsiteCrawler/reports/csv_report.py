import csv


class CSVReport:

    def write_report(self, results, file_path):

        with open(
            file_path,
            mode="w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=["url", "status", "result", "response_time"]
            )

            writer.writeheader()

            writer.writerows(results)