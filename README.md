# JumpStart your [Vector Database](https://weaviate.io/) to enterprise scale with [OKD](httos://okd.io)

## Agenda

### What we will build.
![rag-demo](images/retrieval-augmented-generation.jpg "retrieval augmented generative search")

### What's needed:
- Access to an Openshift developer account.
- A Weaviate service.
- A HuggingFace API key.
- An OpenAI API key.

### Get access to Openshift
- The easiest path is to signup for a [Developer Sandbox](https://developers.redhat.com/developer-sandbox)

### [Install Weaviate](install-weaviate.md) on Openshift

### Benefits of Eclipse-Che/DevSpaces
- A full IDE experience with a code debugger.
- Leverage many VSCode extensions.
- It runs as a pod making network testing easier.
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
```
curl weaviate.your-dev-namespace | jq
```
- Run a few python test clients from the `src` directory.
- Optionally, create a github webhook to trigger Openshift builds.

### Move the app into production.
Create a project using your initials.
```
PROJ=bk-apps
oc new-project $PROJ
```
Create the application.
```
oc new-app python~https://github.com/bkoz/weaviate --context-dir=/src --name=rag
```

Edit the plain text `resources/env-vars.txt` file to reflect your environment.

Create a secret from this file.
```
oc create secret generic myenvs --from-env-file=resources/env-vars.txt
```

Add the secret to the deployment
```
oc set env --from=secret/myenvs deployment/rag
```

Expose the app with a route.
```
oc create route edge --service rag --insecure-policy='Redirect'
```
### Addtional ways to get access to Openshift.
- Create a mini-cluster by [installing Code Ready Containers](https://www.okd.io/crc/)
- Install an [OKD cluster](https://www.okd.io/installation/) and Eclipse-Che.
- Install an [Openshift](https://www.redhat.com/en/technologies/cloud-computing/openshift) cluster and DevSpaces.
