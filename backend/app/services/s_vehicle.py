import os
import uuid

from app.features.vehicle.job import JOBS, Job
from app.services import SSite


class SVehicle:
    def __init__(self, ssite: SSite | None = None) -> None:
        self.ssite = ssite

    def read_jobs(self) -> list[str]:
        return list(JOBS.keys())

    def start_job(self, id: uuid.UUID):
        site = self.ssite.read_site(id)

        model = os.path.join(os.path.abspath(os.getcwd()), site.model)
        region_config = eval(site.polygon), eval(site.line_in), eval(site.line_out)
        job = Job(url_stream=site.url, path_model=model, region_config=region_config)
        job.start()

        JOBS[site.url] = job
