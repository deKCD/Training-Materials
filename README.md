# Training-Materials

This repository is a collection of GTN compatible de.KCD / de.NBI training materials and learning pathways. The content is licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).

Our training materials are designed to help researchers and data scientists learn how to effectively use cloud technologies for data management and processing.

## About de.KCD

de.KCD is a cross-location and cross-domain contact point for teaching skills in handling data using cloud-based technologies, resources and methods for institutions and networked centers as well as for researchers at all career levels. You can find more information about de.KCD on our [website](https://datenkompetenz.cloud/en/). Please check it for upcoming events, news, and further information. Our main GitHub organization is [deKCD](https://github.com/deKCD).

de.KCD is linked through its members to the [German Network for Bioinformatics Infrastructure (de.NBI)](https://www.denbi.de/). 

## Adding new content

If you want to contribute new material, please check our [contribution guide](CONTRIBUTING.md)! We welcome contributions from the community to expand our training materials and learning pathways.

### Running the website locally

To run the website locally, you need to have [Ruby](https://www.ruby-lang.org/en/documentation/installation/) and [Bundler](https://bundler.io/) installed. After that, you can run the following commands:

```bash
# Install the required gems
bundle install 
# Run the Jekyll server
bundle exec jekyll serve --trace --livereload
```

Alternatively, you can use the provided `run.sh` script to start the Jekyll server:

```bash
# Make the script executable
chmod +x run.sh
# Run the script
./run.sh
``` 

Then, open your web browser and navigate to `http://localhost:4000/Training-Materials/` to view the website.

### Running the containerized version

Currently images are being pushed to [quay.io](quay.io/dekcd/) by hand. 
Building and pushing of a new version after changes can be carried out as follows:
```
docker build . -t quay.io/deckd/training-materials:VERSION_NUMBER --push
```
One can also run a local build by running `docker compose -f compose.dev.yml up -d` for testing.
One would need to adjust the `compose.dev.yml` file accordingly.

#### Things to consider with the containerized version

The image allows to retrieve webhooks from GitHub to update the state of the static jekyll site.
One needs to set a webhook secret for this - on default changes for the "main"-branch of the repository are considered. If one wants to adjust the branch that is watched for updates, the `TARGET_BRANCH` variable needs to be adjusted
Have a look on the [compose.dev.yml](./compose.dev.yml)-file to see how the variables and the image is used in compose-setups.
Webhooks will be sent to [https://dekcd.bi.denbi.de/training/webhook](https://dekcd.bi.denbi.de/training/webhook).


To enable the use of the Jekyll-Site in combination with any other webpage, one needs to adjust the configuration, e.g. of HAProxy.
The current haproxy-config looks similar to this:
```
backend dekcd_training
    http-request set-path %[path,regsub(^/training/?,/training/)] 
    server s1 training-material-container-name:4000 check resolvers docker resolve-prefer ipv4 init-addr none

backend dekcd_training_webhook
    http-request set-path %[path,regsub(^/training/webhook?,/webhook)] 
    server s1 training-material-container-name:5000 check resolvers docker resolve-prefer ipv4 init-addr none
```
with `training-test` as the container running the jekyll-site.


### Development with Devcontainer

We provide a devcontainer for easy development and testing of the website. You can find the devcontainer configuration in the `.devcontainer` directory. To use it, you need to have [Visual Studio Code](https://code.visualstudio.com/) installed. Open the repository in VS Code and it will prompt you to reopen the folder in the container. After that, you can run the Jekyll server as described above. 