# Configuration

The Omniport project loads all settings from YAML configuration files. On a Dockerised distribution, the `docker-compose.yml` file takes care of loading the set of these configuration files into the Django container from this directory.

## Instructions

- Use the YAML stencil `base_stencil.yml` to create `base.yml`.
- Go to the `sites` folder.
- For as many sites as you are deploying (plus the development site), use the YAML stencil `site_stencil.yml` to create `site_<site_id>.yml`.
    - In this specific case the following site IDs are being followed.
        - **Site ID 0:** the development site launched by the run script
        - **Site ID 1:** the Intranet facing site
        - **Site ID 2:** the Internet facing site