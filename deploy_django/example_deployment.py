#!/usr/bin/env python3
import os

from deploy_django.deploy_base import Deployment


class Example(Deployment):
    def deploy_hook(self):
        print('Test!')


if __name__ == '__main__':
    print('Start!')
    Example()
