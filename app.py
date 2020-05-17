#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
import click
import re

from flask import Flask
from flask import request
from flask import jsonify

import docker
from docker_helper import DockerHelper
import logging

app = Flask(__name__)
client = docker.from_env()
log = logging.getLogger()
log.addHandler(logging.StreamHandler())
log.setLevel(logging.INFO)


@app.route('/')
def main():
    return jsonify(success=True), 200


@app.route('/images/pull', methods=['POST'])
def image_puller():
    token_val = request.form['token'] if 'token' in request.form else None
    if token_val is None:
        token_val = request.args['token'] if 'token' in request.args else None

    image_val = request.form['image'] if 'image' in request.form else None
    if image_val is None:
        image_val = request.args['image'] if 'image' in request.args else None

    if not token_val or not image_val:
        return jsonify(success=False, error="Missing parameters"), 400

    image = image_val

    if token_val != os.environ['TOKEN']:
        return jsonify(success=False, error="Invalid token"), 403

    restart_containers = request.form['restart_containers'] if 'restart_containers' in request.form else None
    if restart_containers is None:
        restart_containers = request.args['restart_containers'] if 'restart_containers' in request.args else None

    restart_containers = restart_containers == "true"

    # Collect the containers
    old_containers = []
    for container in client.containers.list():
        imagename = container.attrs['Config']['Image']
        if re.match(r'.*' + re.escape(image) + r'$', imagename):
            old_containers.append(container)

    if len(old_containers) is 0:
        return jsonify(success=False, error="No running containers found with the specified image"), 404

    logging.info(f"Updating {str(len(old_containers))} containers with {image} image")
    # Get the directory of the docker-compose service
    for container in old_containers:
        probable_dc_dir = container.labels["com.docker.compose.project.working_dir"]
        service = container.labels["com.docker.compose.service"]
        dh = DockerHelper(probable_dc_dir)
        log.info("Pulling new image")
        dh.pull(service)

    if restart_containers is False:
        return jsonify(success=True, message=str(len(old_containers)) + " containers updated"), 200

    log.info('Recreating containers...')
    for container in old_containers:
        probable_dc_dir = container.labels["com.docker.compose.project.working_dir"]
        service = container.labels["com.docker.compose.service"]
        dh = DockerHelper(probable_dc_dir)
        dh.up(service)

    return jsonify(success=True, message=str(len(old_containers)) + " containers updated and restarted"), 200


@click.command()
@click.option('-h', default='0.0.0.0', help='Set the host')
@click.option('-p', default=8080, help='Set the listening port')
@click.option('--debug', default=False, help='Enable debug option')
def main(h, p, debug):
    if not os.environ.get('TOKEN'):
        print('ERROR: Missing TOKEN env variable')
        sys.exit(1)

    registry_user = os.environ.get('REGISTRY_USER')
    registry_passwd = os.environ.get('REGISTRY_PASSWD')
    registry_url = os.environ.get('REGISTRY_URL', 'https://index.docker.io/v1/')

    if registry_user and registry_passwd:
        try:
            client.login(username=registry_user, password=registry_passwd, registry=registry_url)
        except Exception as e:
            print(e)
            sys.exit(1)

    app.run(
        host=os.environ.get('HOST', default=h),
        port=os.environ.get('PORT', default=p),
        debug=os.environ.get('DEBUG', default=debug)
    )


if __name__ == "__main__":
    main()
