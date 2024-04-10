from graphviz import Digraph
import itertools
from kubernetes import client, config
import get_connections

def list_pods_by_namespace(exclude_namespaces=None):
    if exclude_namespaces is None:
        exclude_namespaces = ["kube-system", "kube-public", "kube-node-lease", "default"]
    
    # Load Kubernetes configuration, e.g., from ~/.kube/config
    config.load_kube_config()

    # Create an instance of the API class
    v1 = client.CoreV1Api()

    # Initialize dictionary to hold namespace: pods data
    cluster_data = {}

    # Retrieve a list of all namespaces
    namespaces = v1.list_namespace()

    for ns in namespaces.items:
        if ns.metadata.name not in exclude_namespaces:
            # Initialize the namespace key in the dictionary
            cluster_data[ns.metadata.name] = []

            # Retrieve a list of all pods within the namespace
            pods = v1.list_namespaced_pod(ns.metadata.name)

            for pod in pods.items:
                # Append pod names to the namespace key in the dictionary
                cluster_data[ns.metadata.name].append(pod.metadata.name)

    return cluster_data

def plot_ns_graph():
    # Define namespaces and pods within them
    cluster_data = list_pods_by_namespace()

    # Define namespace connections
    namespace_connections = get_connections.list_all_network_policies()

    dot = Digraph(comment='Namespaces with connections and fully connected pods',engine='dot')

    # Set graph attributes
    dot.attr(compound='true', rankdir='LR', nodesep='1')

    # Placeholder for namespace center points
    namespace_centers = {}

    for ns, pods in cluster_data.items():
        with dot.subgraph(name=f'cluster_{ns}') as c:
            c.attr(label=ns, style='filled', color='lightgrey', shape='box')
            c.attr('node', shape='circle', style='filled', color='white')
            
            
        #     # Add pods to the namespace and connect them
        #     for pod in pods:
        #         c.node(pod, pod)
        #     for (pod1, pod2) in itertools.combinations(pods, 2):
        #         c.edges([(pod1, pod2), (pod2, pod1)])  # Fully connected pods
            
        # # Assuming the first pod as the namespace center for simplicity
        # namespace_centers[ns] = pods[0]
            
        # Add pods to the namespace and connect them
            if pods:  # Check if the namespace has any pods
                for pod in pods:
                    c.node(pod, pod)
                for (pod1, pod2) in itertools.combinations(pods, 2):
                    c.edges([(pod1, pod2), (pod2, pod1)])   # Fully connected pods
                
                # Assuming the first pod as the namespace center for simplicity
                namespace_centers[ns] = pods[0]
            else:
                # If no pods, create a dummy center for the namespace
                dummy_center = f"{ns}_center"
                c.node(dummy_center, label='No Pods', shape='plaintext')
                namespace_centers[ns] = dummy_center
    # Connect namespaces directly, using a conceptual center or a representative pod
    for ns1, ns2 in namespace_connections:
        center1 = namespace_centers[ns1]
        center2 = namespace_centers[ns2]
        dot.edge(center1, center2, color='red', constraint='false', lhead=f'cluster_{ns2}', ltail=f'cluster_{ns1}')
        dot.edge(center2, center1, color='red', constraint='false', lhead=f'cluster_{ns1}', ltail=f'cluster_{ns2}')


    # Render the graph to a file
    dot.render('namespace_connections', format='png', cleanup=True)

if __name__=='__main__':
    plot_ns_graph()