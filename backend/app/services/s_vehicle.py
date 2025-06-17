from app.features.vehicle.job import JOBS, Job
from app.services import SSite


class SVehicle:
    def __init__(self, ssite: SSite | None = None) -> None:
        self.ssite = ssite

    def read_jobs(self) -> list[str]:
        return list(JOBS.keys())

    def start_job(self):
        # ip-cam
        url = "rtsp://huda:Burunghudhud112@192.168.50.26:554/Streaming/Channels/101/"

        line_in = None
        line_out = [[839, 20], [1157, 1333]]
        polygon = [[1157, 72], [1516, 278], [854, 1101], [707, 146]]
        region_config = (polygon, line_in, line_out)

        path_model = "C:/Users/eats/projects/IASS/asset/result/data_yolo11m_100/detect/train/weights/best.pt"

        job = Job(url_stream=url, path_model=path_model, region_config=region_config)
        job.start()

        JOBS[url] = job
