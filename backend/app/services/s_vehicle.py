import os
import uuid

from app.core.config import settings
from app.features.vehicle.job import JOBS, Job
from app.models import Message
from app.services import SHub, SSite


def frame_generator(job: Job):
    while job.state_streaming.running.is_set():
        frame_bytes = job.state_streaming.frame
        if frame_bytes is None:
            continue

        yield (
            b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n"
        )


class SVehicle:
    def __init__(self, shub: SHub | None = None, ssite: SSite | None = None) -> None:
        self.shub = shub
        self.ssite = ssite

    def read_jobs(self) -> list[str]:
        return list(JOBS.keys())

    def read_job(self, id: uuid.UUID):
        # TODO: add read job service
        site = self.ssite.read_site(id)
        job = JOBS.get(site.id)
        if not job:
            return Message(message="Job not found.")
        return frame_generator(job)

    def create_job(
        self,
        id_site: uuid.UUID,
        id_region: uuid.UUID | None = None,
        fps=20,
        buffer=1,
        is_stream=0,
        verbose=0,
    ) -> Message:
        try:
            hub = self.shub.read_hub_by_name("main")
            site = self.ssite.read_site(id_site)

            url = f"rtsp://{site.username}:{site.password}@{site.host}:{site.port}"
            model = os.path.join(settings.DIR_ASSETS, hub.model)
            region_config = eval(site.polygon), eval(site.line_in), eval(site.line_out)

            job = Job(
                url_stream=url,
                path_model=model,
                region_config=region_config,
                fps=fps,
                buffer=buffer,
                is_stream=is_stream,
                verbose=verbose,
            )
            job.start()

            JOBS[site.id] = job
        except Exception as e:
            return Message(message=f"Error occured: {e}")
        return Message(message="Job added successfully.")

    def delete_job(self, id: uuid.UUID) -> Message:
        site = self.ssite.read_site(id)
        job = JOBS.get(site.id)
        if not job:
            return Message(message="Job not found.")
        job.stop(id)
        return Message(message="Job deleted successfully")
