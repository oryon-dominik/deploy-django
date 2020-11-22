import subprocess

from fastapi import BackgroundTasks, FastAPI

app = FastAPI()


def run_deploy():
    print("running deployment")
    print("deployment complete")
    cmd = subprocess.run("./deploy_cast_hosting.sh", capture_output=True)
    print("stdout: ", cmd.stdout.decode("utf8"))


@app.post("/deploy")
async def deploy(background_tasks: BackgroundTasks):
    print("deploying...")
    background_tasks.add_task(run_deploy)
    return {"message": "deploying"}