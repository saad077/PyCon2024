# Automated Deployment & Testing

CI/CD trigger
1. On-Push: Main 

## Trigger Type-1: On-Push by Manifest Updates

The `main`, and all `demand.ai/*` branches contains their own manifest.yaml files.
The manifest in `main` represents the active/in-progress Demand.AI release.
The manifest in `demand.ai/*` branches represents the previously released Demand.AI versions.

Whenever the `manifest.yaml` file gets updated in any of theses branches, it triggers the automation which does the following;

1. `Detect Manifest Changes & Trigger Deployment` [workflow](https://github.com/Kinaxis/demand-ai/actions/workflows/detect_manifest_changes.yaml) gets triggered which checks for changes in certain fields of the manifest i.e. ais version, aip version, genesis version etc. 
    - This workflow runs in the 'same branch' where the manifest trigger occurred.
1. If changes are detected, the `Sanity Test Deployment` [workflow](https://github.com/Kinaxis/demand-ai/actions/workflows/sanity_test_deployment.yaml)</b> gets triggered which does the deployment, testing and teardown.
    - The `Sanity Test Deployment workflow` always gets triggered in the `main` branch. This is to keep all the deployment / testing related code, configs, and helper scripts in one place for easy maintenance and updates.
    - The `Sanity Test Deployment workflow` uses the `manifest_version` input, passed by the triggering `Detect Manifest Changes & Trigger Deployment` to know which manifest version to use for deployment

## Trigger Type-2: On-schedule using Master/Latest Code

This is triggered every weekday using the versions specified in the `manifest-dev.yaml` file in the `main` branch.
It triggers the `Sanity Test Deployment` [workflow](https://github.com/Kinaxis/demand-ai/actions/workflows/sanity_test_deployment.yaml) in `main` with the `Latest_Code` option.

## Other Details
More details on the automation, and the overall process can be found on this confluence page: [Demand.AI Deployment and Testing Pipeline](https://confluence.kinaxis.com/x/qIw6Dg) 

## Future Work
Some of the major future updates to this automation / pipeline include;
1. Extend the pipeline to include full E2E deployment i.e. RR, ES, FS, EA etc. and run full E2E Testing (GHA owned by Yong/Saad) post deployment
1. Once [Move Jijna Templates out of Application Deployment](https://jira.kinaxis.com/browse/PE-7979) is completed, move all deployment automation workflows to directly use the GHAs in `application-deployment` repo. At that point, the `demand-ai` will only contain the manifest files, and the `Detect Manifest Changes & Trigger Deployment` which will detect changes and trigger deployment / testing directly in `application-deployment`