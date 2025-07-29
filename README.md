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
bundle exec jekyll serve --trace --reload
```

Alternatively, you can use the provided `run.sh` script to start the Jekyll server:

```bash
# Make the script executable
chmod +x run.sh
# Run the script
./run.sh
``` 

### Development with Devcontainer

We provide a devcontainer for easy development and testing of the website. You can find the devcontainer configuration in the `.devcontainer` directory. To use it, you need to have [Visual Studio Code](https://code.visualstudio.com/) installed. Open the repository in VS Code and it will prompt you to reopen the folder in the container. After that, you can run the Jekyll server as described above. 