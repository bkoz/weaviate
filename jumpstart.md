# JumpStart your [Vector Database](https://weaviate.io/) to enterprise scale with [OKD](httos://okd.io)

## Agenda

### Different ways to get access to Openshift
- The easiest path is to signup for a [Developer Sandbox](https://developers.redhat.com/developer-sandbox)
- Or create a mini-cluster by [installing Code Ready Containers](https://www.okd.io/crc/)
- Or create a community cluster by [installing OKD](https://www.okd.io/installation/) and the [Eclipse-Che] operator.
- Or create an [Openshift](https://www.redhat.com/en/technologies/cloud-computing/openshift) cluster and the [DevSpaces] operator.

### [Install Weaviate](README.md)

### Benefits of DevSpaces
- A full IDE experience with a debugger.
- Leverage many VSCode extensions.
- Running as a pod makes network testing easier.
- Deploy and test your app with port forwarding.
- GitHub integration improves workflow efficiency.
- Environment variables are read in as secrets.
- The price is right.

### Install the Eclipse-Che/
### Developer Workflow with Eclipse-Che/DevSpaces
- Launch the Eclipse-Che/DevSpaces dashboard.
- Add a new workspace by cloning https://github.com/bkoz/weaviate
- Install the VSCode python extension.
- Create a python virtual environment.
- Open a terminal.
- Test the weaviate service.
```
curl ${WEAVIATE_URL} | jq
```
- Run a few python test clients.
- Optionally, create a github webhook to trigger Openshift builds.

### Move the app into production
```
oc new-app python~https://github.com/bkoz/weaviate --context-dir=/src --name=rag
```

Create a test file containing the following environment variables.
```
WEAVIATE_URL=${WEAVIATE_URL}
WEAVIATE_API_KEY=${WEAVIATE_API_KEY} 
HUGGINGFACE_API_KEY=${HUGGINGFACE_API_KEY}
OPENAI_API_KEY=${OPENAI_API_KEY}
```

Create a secret from this file.
```
oc create secret generic myenvs --from-env-file=/var/tmp/myenvs
```

Add the secret to the deployment
```
oc set env --from=secret/myenvs deployment/rag
```

Expose the app with a route.
```
oc create route edge --service rag --insecure-policy='Redirect'
```