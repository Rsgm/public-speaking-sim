#!/bin/bash
echo Installing CI runner
curl -L https://packages.gitlab.com/install/repositories/runner/gitlab-ci-multi-runner/script.deb.sh | sudo bash
sudo apt-get install gitlab-ci-multi-runner
echo CI runner installed, now configuring runner
expect "Please enter the gitlab-ci coordinator URL (e.g. https://gitlab.com/ci):"
send "https://gitlab.com/ci"
expect "Please enter the gitlab-ci token for this runner:"
send "J938AD4ZcarLsFXYP-Ez"
expect "Please enter the gitlab-ci description for this runner:"
send "Django runner"
expect "Please enter the gitlab-ci tags for this runner (comma separated):"
send "django,test,site"
expect "Please enter the executor: shell, ssh, virtualbox, docker+machine, docker-ssh+machine, docker, docker-ssh, parallels:"
send "docker"
expect "Please enter the default Docker image (eg. ruby:2.1):"
send "django:3.9"
echo Runner registered successfully. Feel free to start it, but if it\'s running already the config should be automatically reloaded!
echo Runner is configured and ready for commits
