from invoke import task

@task
def test(ctx):
    ctx.run("pytest src")

@task
def coverage_report(ctx):
    ctx.run("coverage run --branch -m pytest src")
    ctx.run("coverage html")

@task
def lint(ctx):
    ctx.run("pylint src")

@task
def start(ctx, web=False):
    with ctx.cd("src"):
        if web:
            ctx.run("flask run --host 0.0.0.0 --port 8080")
        else:
            ctx.run("python main.py")
