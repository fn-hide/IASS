# FastAPI Project - Backend

## TODO

- [x] 🍻 Copy and paste from IASSEdge backend
- [x] 🔧 Update default hub url
- [x] 🗃️ Make item table to store a vehicle counting object
- [x] 🔧 Add pycharm configuration
- [x] 🗃️ Re-generate migration files with order prefix
- [x] 🐛 Fix can't insert into a database by replacing SessionDep with general session
- [x] ✨ Add connect timeout exception handler
- [x] 💡 Comment background task (only for edge backend)
- [x] ✨ Add an api to send item into hub
- [x] 🛂 Change item:create permission for all users
- [x] ✨ Add a background task to create edge user
- [x] 🗃️ Split `url` column into `host` and `port` columns
- [x] 🗃️ Add a `limit_send` limit to send into hub
- [x] 🚚 Rename `ping_hub_interval` into `interval_ping`
- [x] 🚚 Rename `DEFAULT_HUB_PING_INTERVAL` into `DEFAULT_HUB_INTERVAL_PING`
- [x] ✏️ Resolve port typo
- [x] 📄 Add MIT license
- [x] ⚗️ Add streaming only
- [x] 🐛 Prevent backend stopped when failed to create edge user
- [x] ➕ Add pytorch cuda 118 dependency
- [x] 🚚 Move pyproject.toml and uv.lock into backend directory
- [x] 🚚 Rename notebook to development
- [x] ✨ Add adjust site region function
- [x] ➕ Add numpy and onnxruntime-gpu
- [x] ✨ Add path, format, and name on export script
- [x] ✨ Add thread for vehicle streamer and counter
- [x] ✨ Add is_counter param to hide heavy computation
- [x] ✨ Add skip frame to prevent drop/broke frame
- [x] ✨ Add custom display counts method
- [x] 📌 Pin onnxruntime-gpu to specific version, i.e. onnxruntime-gpu==1.18.0
- [x] 🍱 Add ip-cam
- [x] 📦️ Export onnx with dynamic, nms, device, half, and batch
- [x] ✨ Return track id, datetime, cls, conf, and count type
- [x] 🧵 Add threading lock for VehicleBase, the child of ObjectCounter
- [x] 🚚 Rename vehicle_main.py into vehicle_job.py
- [x] ✨ Add VehicleJob class
- [x] 🚚 Organize and rename realtime feature
- [x] 🚚 Move realtime to vehicle_counter
- [x] ✨ Add an api for realtime vehicle counter
- [x] 🗃️ Add track id, rename identity_index, and add track id
- [x] ✨ Add api to count vehicle from CCTV (site) in real-time (with threads)
- [x] ✨ Insert detected vehicle into database at realtime
- [x] 🗃️ Add line in, line out, and polygon
- [x] ✨ Add auto-clear item if item data is_up
- [x] ✨ Add vehicles api and receive the id parameter
- [x] 🔧 Add directory in pydantic settings
- [x] 🗃️ Explode url into username, password, host, and port
- [x] 🗃️ Remove address from site table
- [x] ✏️ Resolve typo in model type of scheme
- [x] ✨ Add hubs api
- [x] 🏷️ Add return type of start job service
- [x] ✨ Add get by condition in repository
- [x] ✨ Add model download api
- [x] 🗃️ Refactor interval ping into sync interval and limit send into sync size
- [x] 🔧 Refactor default hub name from pangsud into main
- [x] 🗃️ Move model column from site into hub
- [x] 💬 Update model not found message
- [x] 🔧 Add directories initialization
- [x] 🔧 Change postgres port inside host from 5432 into 5433
- [x] 🐛 Fix missing query of model attribute
- [x] ➖ Revert dependencies to base requirement without cuda
- [x] ♻️ Wrap inference in class
- [x] ⚡️ Add crop and mask to be more efficient
- [x] 🐛 Fix site has no attribute url
- [x] ✨ Add verbose as parameter for debugging purpose
- [x] ♻️ Change site url into site id as key of JOBS
- [x] ✨ Add feature to remove running thread of vehicle counting
- [x] 🔧 Back to the original configuration
- [x] ➕ Add opencv dependencies
- [x] ➕ Add ultralytics dependencies
- [x] 📝 Add preparation
- [x] 📝 Improve markdown
- [x] ➕ Add clip and openvino for production
- [x] ➕ Add plotly, nbformat, and seaborn for development
- [x] ⚗️ Generate coral fps over time
- [x] 🧵 Fix database engine creation
- [x] ✨ Add api for streaming
- [x] 🐛 Fix count label is still showing in streaming
- [x] 🏗️ Use uvicorn instead of fastapi to run backend
- [x] 🔨 Comment tasks for main server
- [x] ♻️ Use `__call__` magic method instead off `process` method
- [x] 🚚 Rename state and buffer into state counting and state streaming
- [x] ✨ Add fps in site input to mirror the site fps
- [x] 🐛 Make date created as created in the system and date stamped as created in the track
- [x] ✨ Drop a frame when queue is full
- [x] ✏️ Resolve state counting typo
- [x] ✨ Add api to get site sample
- [x] 💄 Change line out colour to pastel purple
- [x] 💄 Add ROI visualization
- [x] 💄 Add start time and duration
- [x] ➕ Add humanize
- [x] 🔧 Update hub host into server 66
- [ ] 🏗️ Make difference branch for site and production use
- [ ] ✨ Add more information for job's object in api response
- [ ] ✨ Add ROI visualization in streaming view
- [ ] ⚡️ Use `gstreamer` instead of OpenCV default streamer
- [ ] 👷 Auto-update edge server by git

## Requirements

    * [Docker](https://www.docker.com/).
    * [uv](https://docs.astral.sh/uv/) for Python package and environment management.

## Docker Compose

Start the local development environment with Docker Compose following the guide in [../development.md](../development.md).

## General Workflow

By default, the dependencies are managed with [uv](https://docs.astral.sh/uv/), go there and install it.

From `./backend/` you can install all the dependencies with:

    ```console
    $ uv sync
    ```

Then you can activate the virtual environment with:

    ```console
    $ source .venv/bin/activate
    ```

Make sure your editor is using the correct Python virtual environment, with the interpreter at `backend/.venv/bin/python`.

Modify or add SQLModel models for data and SQL tables in `./backend/app/models.py`, API endpoints in `./backend/app/api/`, CRUD (Create, Read, Update, Delete) utils in `./backend/app/crud.py`.

## VS Code

There are already configurations in place to run the backend through the VS Code debugger, so that you can use breakpoints, pause and explore variables, etc.

The setup is also already configured so you can run the tests through the VS Code Python tests tab.

## Docker Compose Override

During development, you can change Docker Compose settings that will only affect the local development environment in the file `docker-compose.override.yml`.

The changes to that file only affect the local development environment, not the production environment. So, you can add "temporary" changes that help the development workflow.

For example, the directory with the backend code is synchronized in the Docker container, copying the code you change live to the directory inside the container. That allows you to test your changes right away, without having to build the Docker image again. It should only be done during development, for production, you should build the Docker image with a recent version of the backend code. But during development, it allows you to iterate very fast.

There is also a command override that runs `fastapi run --reload` instead of the default `fastapi run`. It starts a single server process (instead of multiple, as would be for production) and reloads the process whenever the code changes. Have in mind that if you have a syntax error and save the Python file, it will break and exit, and the container will stop. After that, you can restart the container by fixing the error and running again:

    ```console
    $ docker compose watch
    ```

There is also a commented out `command` override, you can uncomment it and comment the default one. It makes the backend container run a process that does "nothing", but keeps the container alive. That allows you to get inside your running container and execute commands inside, for example a Python interpreter to test installed dependencies, or start the development server that reloads when it detects changes.

To get inside the container with a `bash` session you can start the stack with:

    ```console
    $ docker compose watch
    ```

and then in another terminal, `exec` inside the running container:

    ```console
    $ docker compose exec backend bash
    ```

You should see an output like:

    ```console
    root@7f2607af31c3:/app#
    ```

that means that you are in a `bash` session inside your container, as a `root` user, under the `/app` directory, this directory has another directory called "app" inside, that's where your code lives inside the container: `/app/app`.

There you can use the `fastapi run --reload` command to run the debug live reloading server.

    ```console
    $ fastapi run --reload app/main.py
    ```

...it will look like:

    ```console
    root@7f2607af31c3:/app# fastapi run --reload app/main.py
    ```

and then hit enter. That runs the live reloading server that auto reloads when it detects code changes.

Nevertheless, if it doesn't detect a change but a syntax error, it will just stop with an error. But as the container is still alive and you are in a Bash session, you can quickly restart it after fixing the error, running the same command ("up arrow" and "Enter").

...this previous detail is what makes it useful to have the container alive doing nothing and then, in a Bash session, make it run the live reload server.

## Backend tests

To test the backend run:

    ```console
    $ bash ./scripts/test.sh
    ```

The tests run with Pytest, modify and add tests to `./backend/app/tests/`.

If you use GitHub Actions the tests will run automatically.

### Test running stack

If your stack is already up and you just want to run the tests, you can use:

    ```bash
    docker compose exec backend bash scripts/tests-start.sh
    ```

That `/app/scripts/tests-start.sh` script just calls `pytest` after making sure that the rest of the stack is running. If you need to pass extra arguments to `pytest`, you can pass them to that command and they will be forwarded.

For example, to stop on first error:

    ```bash
    docker compose exec backend bash scripts/tests-start.sh -x
    ```

### Test Coverage

When the tests are run, a file `htmlcov/index.html` is generated, you can open it in your browser to see the coverage of the tests.

## Migrations

As during local development your app directory is mounted as a volume inside the container, you can also run the migrations with `alembic` commands inside the container and the migration code will be in your app directory (instead of being only inside the container). So you can add it to your git repository.

Make sure you create a "revision" of your models and that you "upgrade" your database with that revision every time you change them. As this is what will update the tables in your database. Otherwise, your application will have errors.

    * Start an interactive session in the backend container:

    ```console
    $ docker compose exec backend bash
    ```

    * Alembic is already configured to import your SQLModel models from `./backend/app/models.py`.

    * After changing a model (for example, adding a column), inside the container, create a revision, e.g.:

    ```console
    $ alembic revision --autogenerate -m "Add column last_name to User model"
    ```

    * Commit to the git repository the files generated in the alembic directory.

    * After creating the revision, run the migration in the database (this is what will actually change the database):

    ```console
    $ alembic upgrade head
    ```

If you don't want to use migrations at all, uncomment the lines in the file at `./backend/app/core/db.py` that end in:

    ```python
    SQLModel.metadata.create_all(engine)
    ```

and comment the line in the file `scripts/prestart.sh` that contains:

    ```console
    $ alembic upgrade head
    ```

If you don't want to start with the default models and want to remove them / modify them, from the beginning, without having any previous revision, you can remove the revision files (`.py` Python files) under `./backend/app/alembic/versions/`. And then create a first migration as described above.

## Email Templates

The email templates are in `./backend/app/email-templates/`. Here, there are two directories: `build` and `src`. The `src` directory contains the source files that are used to build the final email templates. The `build` directory contains the final email templates that are used by the application.

Before continuing, ensure you have the [MJML extension](https://marketplace.visualstudio.com/items?itemName=attilabuti.vscode-mjml) installed in your VS Code.

Once you have the MJML extension installed, you can create a new email template in the `src` directory. After creating the new email template and with the `.mjml` file open in your editor, open the command palette with `Ctrl+Shift+P` and search for `MJML: Export to HTML`. This will convert the `.mjml` file to a `.html` file and now you can save it in the build directory.
