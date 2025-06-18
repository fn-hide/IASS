import os
import uuid

from app.core.config import settings
from app.features.vehicle.job import JOBS, Job
from app.models import Message
from app.services import SSite


class SVehicle:
    def __init__(self, ssite: SSite | None = None) -> None:
        self.ssite = ssite

    def read_jobs(self) -> list[str]:
        return list(JOBS.keys())

    def start_job(self, id: uuid.UUID):
        try:
            site = self.ssite.read_site(id)

            url = f"rtsp://{site.username}:{site.password}@{site.host}:{site.port}"
            model = os.path.join(settings.DIR_ASSETS, site.model)
            region_config = eval(site.polygon), eval(site.line_in), eval(site.line_out)

            job = Job(url_stream=url, path_model=model, region_config=region_config)
            job.start()

            JOBS[site.url] = job
        except Exception as e:
            return Message(message=f"Error occured: {e}")
        return Message(message="Job added successfully.")
