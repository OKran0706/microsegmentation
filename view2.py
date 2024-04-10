from kubernetes import client, config
from graphviz import Digraph
import itertools

# Load kubeconfig
config.load_kube_config()

# Create a Kubernetes API client
v1 = client.CoreV1Api()

# Retrieve all namespaces
namespaces = v1.list_namespace()

# Initialize Graphviz Digraph
dot = Digraph(comment='Kubernetes Namespaces and Pods')
dot.attr(compound='true', rankdir='LR', nodesep='1')

# Loop through namespaces
for ns in namespaces.items:
    ns_name = ns.metadata.name
    with dot.subgraph(name=f'cluster_{ns_name}') as c:
        c.attr(label=ns_name, style='filled', color='lightgrey', shape='box')
        c.attr('node', shape='circle', style='filled', color='white')
        
        # Retrieve all pods in the current namespace
        pods = v1.list_namespaced_pod(ns_name)
        
        # Add pods to the namespace and connect them
        pod_names = [pod.metadata.name for pod in pods.items]
        for pod_name in pod_names:
            c.node(pod_name, pod_name)
        for (pod1, pod2) in itertools.combinations(pod_names, 2):
            c.edges([(pod1, pod2), (pod2, pod1)])  # Fully connected pods

# This example does not automatically add inter-namespace connections.
# You would need to derive logic for connecting namespaces based on your criteria,
# such as network policies, service exposure, or manual configuration.

# Render the graph to a file
dot.render('kubernetes_namespace_pod_connectivity', format='png', cleanup=True)

