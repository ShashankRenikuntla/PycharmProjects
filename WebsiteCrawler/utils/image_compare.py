import cv2
import numpy as np


class ImageCompare:

    def __init__(self, staging_image, production_image, threshold=5.0):
        self.staging_image = staging_image
        self.production_image = production_image
        self.threshold = threshold

    def compare(self):

        staging = cv2.imread(self.staging_image)
        production = cv2.imread(self.production_image)

        print("================================")
        print("IMAGE COMPARISON")
        print("================================")

        print("Staging Image:", self.staging_image)
        print("Production Image:", self.production_image)

        # --------------------------------------------------
        # 1. Check images
        # --------------------------------------------------

        if staging is None:
            print("Staging image could not be loaded")

            return {
                "result": "FAIL",
                "changed_percentage": None,
                "threshold": self.threshold,
                "meaningful_differences": 0,
                "difference_image": None
            }

        if production is None:
            print("Production image could not be loaded")

            return {
                "result": "FAIL",
                "changed_percentage": None,
                "threshold": self.threshold,
                "meaningful_differences": 0,
                "difference_image": None
            }

        print("Staging Loaded: True")
        print("Production Loaded: True")

        staging_height, staging_width = staging.shape[:2]
        production_height, production_width = production.shape[:2]

        print(
            "Staging Size:",
            staging_width,
            "x",
            staging_height
        )

        print(
            "Production Size:",
            production_width,
            "x",
            production_height
        )

        # --------------------------------------------------
        # 2. Full comparison canvas
        # --------------------------------------------------

        comparison_width = max(
            staging_width,
            production_width
        )

        comparison_height = max(
            staging_height,
            production_height
        )

        print(
            "Full Comparison Size:",
            f"{comparison_width} x {comparison_height}"
        )

        # --------------------------------------------------
        # 3. Create full-size canvases
        # --------------------------------------------------

        staging_canvas = np.full(
            (
                comparison_height,
                comparison_width,
                3
            ),
            255,
            dtype=np.uint8
        )

        production_canvas = np.full(
            (
                comparison_height,
                comparison_width,
                3
            ),
            255,
            dtype=np.uint8
        )

        # --------------------------------------------------
        # 4. Put screenshots on canvas
        # --------------------------------------------------

        staging_canvas[
            0:staging_height,
            0:staging_width
        ] = staging

        production_canvas[
            0:production_height,
            0:production_width
        ] = production

        # --------------------------------------------------
        # 5. Page size differences
        # --------------------------------------------------

        height_difference = abs(
            staging_height - production_height
        )

        width_difference = abs(
            staging_width - production_width
        )

        print(
            "Height Difference:",
            f"{height_difference}px"
        )

        print(
            "Width Difference:",
            f"{width_difference}px"
        )

        # --------------------------------------------------
        # 6. Reduce image size for visual analysis
        #
        # This helps ignore tiny font/rendering differences.
        # --------------------------------------------------

        analysis_scale = 0.33

        analysis_width = max(
            1,
            int(comparison_width * analysis_scale)
        )

        analysis_height = max(
            1,
            int(comparison_height * analysis_scale)
        )

        staging_analysis = cv2.resize(
            staging_canvas,
            (
                analysis_width,
                analysis_height
            ),
            interpolation=cv2.INTER_AREA
        )

        production_analysis = cv2.resize(
            production_canvas,
            (
                analysis_width,
                analysis_height
            ),
            interpolation=cv2.INTER_AREA
        )

        print(
            "Visual Analysis Size:",
            f"{analysis_width} x {analysis_height}"
        )

        # --------------------------------------------------
        # 7. Blur small rendering differences
        # --------------------------------------------------

        staging_blur = cv2.GaussianBlur(
            staging_analysis,
            (5, 5),
            0
        )

        production_blur = cv2.GaussianBlur(
            production_analysis,
            (5, 5),
            0
        )

        # --------------------------------------------------
        # 8. Calculate visual difference
        # --------------------------------------------------

        difference = cv2.absdiff(
            staging_blur,
            production_blur
        )

        difference = np.max(
            difference,
            axis=2
        ).astype(np.uint8)

        # --------------------------------------------------
        # 9. Ignore small pixel differences
        # --------------------------------------------------

        _, difference_mask = cv2.threshold(
            difference,
            40,
            255,
            cv2.THRESH_BINARY
        )

        # --------------------------------------------------
        # 10. Remove small noise
        # --------------------------------------------------

        small_kernel = cv2.getStructuringElement(
            cv2.MORPH_RECT,
            (3, 3)
        )

        difference_mask = cv2.morphologyEx(
            difference_mask,
            cv2.MORPH_OPEN,
            small_kernel
        )

        # --------------------------------------------------
        # 11. Join nearby differences
        # --------------------------------------------------

        large_kernel = cv2.getStructuringElement(
            cv2.MORPH_RECT,
            (7, 7)
        )

        difference_mask = cv2.morphologyEx(
            difference_mask,
            cv2.MORPH_CLOSE,
            large_kernel
        )

        # --------------------------------------------------
        # 12. Find visual difference regions
        # --------------------------------------------------

        contours, _ = cv2.findContours(
            difference_mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        # Minimum area at reduced analysis scale
        minimum_area = 50

        meaningful_mask = np.zeros_like(
            difference_mask
        )

        meaningful_differences = 0

        # --------------------------------------------------
        # 13. Draw major differences on full-size image
        # --------------------------------------------------

        difference_image = staging_canvas.copy()

        for contour in contours:

            area = cv2.contourArea(contour)

            if area < minimum_area:
                continue

            meaningful_differences += 1

            # Difference region on analysis image
            x, y, width, height = cv2.boundingRect(
                contour
            )

            # Add region to mask
            cv2.drawContours(
                meaningful_mask,
                [contour],
                -1,
                255,
                -1
            )

            # Convert reduced coordinates
            # back to full screenshot coordinates
            full_x = int(
                x / analysis_scale
            )

            full_y = int(
                y / analysis_scale
            )

            full_width = int(
                width / analysis_scale
            )

            full_height = int(
                height / analysis_scale
            )

            # Draw rectangle on full-size screenshot
            cv2.rectangle(
                difference_image,
                (
                    full_x,
                    full_y
                ),
                (
                    full_x + full_width,
                    full_y + full_height
                ),
                (0, 0, 255),
                3
            )

        # --------------------------------------------------
        # 14. Calculate changed area
        # --------------------------------------------------

        different_pixels = cv2.countNonZero(
            meaningful_mask
        )

        total_pixels = (
            meaningful_mask.shape[0]
            * meaningful_mask.shape[1]
        )

        if total_pixels == 0:

            changed_percentage = 0

        else:

            changed_percentage = (
                different_pixels / total_pixels
            ) * 100

        # --------------------------------------------------
        # 15. Save full-pages difference image
        # --------------------------------------------------

        difference_path = "reports/image_diff.png"

        cv2.imwrite(
            difference_path,
            difference_image
        )

        # --------------------------------------------------
        # 16. PASS / FAIL
        # --------------------------------------------------

        if changed_percentage <= self.threshold:

            result = "PASS"

        else:

            result = "FAIL"

        # --------------------------------------------------
        # 17. Report
        # --------------------------------------------------

        print(
            f"Changed Area: {changed_percentage:.2f}%"
        )

        print(
            f"Threshold: {self.threshold:.2f}%"
        )

        print(
            "Meaningful Differences:",
            meaningful_differences
        )

        print(
            "Difference Image:",
            difference_path
        )

        print(
            f"Result: {result}"
        )

        print("================================")

        # --------------------------------------------------
        # 18. Return result
        # --------------------------------------------------

        return {
            "result": result,
            "changed_percentage": round(
                changed_percentage,
                2
            ),
            "threshold": self.threshold,
            "meaningful_differences":
                meaningful_differences,
            "difference_image":
                difference_path
        }