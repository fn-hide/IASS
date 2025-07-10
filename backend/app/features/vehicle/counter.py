import threading

from ultralytics.solutions import ObjectCounter
from ultralytics.solutions.solutions import SolutionAnnotator, SolutionResults
from ultralytics.utils.plotting import colors

from app.utils import utcnow


class Counter(ObjectCounter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lock = threading.Lock()

    def count_objects(
        self,
        current_centroid: tuple[float, float],
        track_id: int,
        prev_position: tuple[float, float] | None,
        cls: int,
    ) -> bool | None:
        """
        Count objects within a polygonal or linear region based on their tracks.

        Args:
            current_centroid (Tuple[float, float]): Current centroid coordinates (x, y) in the current frame.
            track_id (int): Unique identifier for the tracked object.
            prev_position (Tuple[float, float], optional): Last frame position coordinates (x, y) of the track.
            cls (int): Class index for classwise count updates.

        Examples:
            >>> counter = ObjectCounter()
            >>> track_line = {1: [100, 200], 2: [110, 210], 3: [120, 220]}
            >>> box = [130, 230, 150, 250]
            >>> track_id_num = 1
            >>> previous_position = (120, 220)
            >>> class_to_count = 0  # In COCO model, class 0 = person
            >>> counter.count_objects((140, 240), track_id_num, previous_position, class_to_count)
        """
        if prev_position is None or track_id in self.counted_ids:
            return

        if len(self.region) == 2:  # Linear region (defined as a line segment)
            if self.r_s.intersects(self.LineString([prev_position, current_centroid])):
                # Determine orientation of the region (vertical or horizontal)
                if abs(self.region[0][0] - self.region[1][0]) < abs(
                    self.region[0][1] - self.region[1][1]
                ):
                    # Vertical region: Compare x-coordinates to determine direction
                    if current_centroid[0] > prev_position[0]:  # Moving right
                        self.in_count += 1
                        self.classwise_counts[self.names[cls]]["IN"] += 1
                        self.counted_ids.append(track_id)
                        return False
                    else:  # Moving left
                        self.out_count += 1
                        self.classwise_counts[self.names[cls]]["OUT"] += 1
                        self.counted_ids.append(track_id)
                        return True
                # Horizontal region: Compare y-coordinates to determine direction
                elif current_centroid[1] > prev_position[1]:  # Moving downward
                    self.in_count += 1
                    self.classwise_counts[self.names[cls]]["IN"] += 1
                    self.counted_ids.append(track_id)
                    return False
                else:  # Moving upward
                    self.out_count += 1
                    self.classwise_counts[self.names[cls]]["OUT"] += 1
                    self.counted_ids.append(track_id)
                    return True

        elif len(self.region) > 2:  # Polygonal region
            if self.r_s.contains(self.Point(current_centroid)):
                # Determine motion direction for vertical or horizontal polygons
                region_width = max(p[0] for p in self.region) - min(
                    p[0] for p in self.region
                )
                region_height = max(p[1] for p in self.region) - min(
                    p[1] for p in self.region
                )

                if (
                    region_width < region_height
                    and current_centroid[0] > prev_position[0]
                    or region_width >= region_height
                    and current_centroid[1] > prev_position[1]
                ):  # Moving right or downward
                    self.in_count += 1
                    self.classwise_counts[self.names[cls]]["IN"] += 1
                    self.counted_ids.append(track_id)
                    return False
                else:  # Moving left or upward
                    self.out_count += 1
                    self.classwise_counts[self.names[cls]]["OUT"] += 1
                    self.counted_ids.append(track_id)
                    return True

    def process(self, im0):
        """
        Process input data (frames or object tracks) and update object counts.

        This method initializes the counting region, extracts tracks, draws bounding boxes and regions, updates
        object counts, and displays the results on the input image.

        Args:
            im0 (numpy.ndarray): The input image or frame to be processed.

        Returns:
            (SolutionResults): Contains processed image `im0`, 'in_count' (int, count of objects entering the region),
                'out_count' (int, count of objects exiting the region), 'classwise_count' (dict, per-class object count),
                and 'total_tracks' (int, total number of tracked objects).

        Examples:
            >>> counter = ObjectCounter()
            >>> frame = cv2.imread("path/to/image.jpg")
            >>> results = counter.process(frame)
        """
        if not self.region_initialized:
            self.initialize_region()
            self.region_initialized = True

        self.extract_tracks(im0)  # Extract tracks
        self.annotator = SolutionAnnotator(
            im0, line_width=self.line_width
        )  # Initialize annotator

        self.annotator.draw_region(
            reg_pts=self.region, color=(208, 0, 104), thickness=self.line_width * 2
        )  # Draw region

        # Iterate over bounding boxes, track ids and classes index
        list_counted = []
        for box, track_id, cls, conf in zip(
            self.boxes, self.track_ids, self.clss, self.confs, strict=False
        ):
            # Draw bounding box and counting region
            self.annotator.box_label(
                box,
                label=self.adjust_box_label(cls, conf, track_id),
                color=colors(cls, True),
            )
            self.store_tracking_history(track_id, box)  # Store track history

            # Store previous position of track for object counting
            prev_position = None
            if len(self.track_history[track_id]) > 1:
                prev_position = self.track_history[track_id][-2]
            counted = self.count_objects(
                self.track_history[track_id][-1], track_id, prev_position, cls
            )  # object counting
            if counted is not None:
                list_counted.append((track_id, utcnow(), cls, conf, counted))

        plot_im = self.annotator.result()
        # self.display_counts(plot_im)  # Display the counts on the frame
        # self.display_output(plot_im)  # Display output with base class function

        # Return SolutionResults
        return SolutionResults(
            plot_im=plot_im,
            in_count=self.in_count,
            out_count=self.out_count,
            classwise_count=dict(self.classwise_counts),
            total_tracks=len(self.track_ids),
        ), list_counted
