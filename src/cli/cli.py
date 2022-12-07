# Command line tool to manage Portfolio built using Click
import click


@click.group()
def admin():
    pass


@admin.command()
def setup():
    """Initial Setup"""
    click.echo('Setting up files required for the service')


@admin.command()
def configure():
    """Configures Settings"""
    click.echo('Going into configuration mode')


@admin.command()
def run():
    """Runs the service locally"""
    click.echo('Running the service on localhost')


@admin.command()
def deploy():
    """Deploys the service"""
    click.echo('Deploying the service')


@admin.command()
@click.argument('users', nargs=-1, required=False)
@click.option('--bulk', '-b', 'files', multiple=True, help="Reads users from file and adds all of them to the database")
def add(users, files):
    """Adds user to database"""
    for user in users:
        click.echo(f'adding user {user}')

    for file in files:
        click.echo(f'reading users from {file}')


if __name__ == '__main__':
    admin()
