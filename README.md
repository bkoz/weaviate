# JumpStart your [Vector Database](https://weaviate.io/) to enterprise scale with [Openshift OKD](httos://okd.io)

## Agenda

### What we will build.
![rag-demo](images/retrieval-augmented-generation.jpg "retrieval augmented generative search")

### What's needed:
- Access to an Openshift developer account.
- A Weaviate service.
- A HuggingFace API key.
- An OpenAI API key.

### Weaviate On Openshift
- Support for [Distributed Architectures](https://weaviate.io/developers/weaviate/concepts/replication-architecture).
- A Great Developer Experience (Easily move code -> containers)
- Security (Doesn't run your containers as root)

### Get access to Openshift
- The easiest path is to signup for a [Developer Sandbox](https://developers.redhat.com/developer-sandbox)

### [Install Weaviate](install-weaviate.md) on Openshift

### Developer Tools: Eclipse-Che/DevSpaces
- A full IDE experience with a code debugger.
- Leverage many VSCode extensions.
- Runs as a pod making for easier service discovery.
- Deploy and test your app with port forwarding.
- GitHub integration improves workflow efficiency.
- Environment variables are read in as secrets.
- The price is right.

#### Developer Workflow with Eclipse-Che/DevSpaces
- Login to Openshift and launch the Eclipse-Che/DevSpaces dashboard.
- Add a new workspace by cloning https://github.com/bkoz/weaviate
- Install the reccomended VSCode python extension.
- Create a python virtual environment. (View -> Command Pallette -> Run Task -> devfile)
- Open a terminal within VSCode.
- Test the weaviate service.
```bash
curl weaviate.your-dev-namespace | jq
```
- Run a few python test clients from the `src` directory.
- Optionally, create a github webhook to trigger Openshift builds.

### Move the app into production.
Create a project using your initials. The Developer Sandbox won't let you create new projects so you can 
skip this step and just use the namespace that you are given.
```bash
PROJ=bk-apps
oc new-project $PROJ
```
Create the application.
```bash
oc new-app python~https://github.com/bkoz/weaviate --context-dir=/src --name=rag
```
Make a copy of the plain text `resources/env-vars.txt` file to a temporary directory (`/var/tmp`). Edit it to reflect your environment.

Create a secret from this file.
```bash
oc create secret generic myenvs --from-env-file=/var/tmp/env-vars.txt
```
Add the secret to the deployment
```bash
oc set env --from=secret/myenvs deployment/rag
```
Expose the app with a route.
```bash
oc create route edge --service rag --insecure-policy='Redirect'
```
### Additional ways to get access to Openshift.
- Create a mini-cluster by [installing Code Ready Containers](https://www.okd.io/crc/)
- Install an [OKD cluster](https://www.okd.io/installation/) and Eclipse-Che.
- Install an [Openshift](https://www.redhat.com/en/technologies/cloud-computing/openshift) cluster and DevSpaces.
- As a managed service from any of the major cloud providers.

#### Versions
v0.1.0
