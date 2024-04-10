from kubernetes import client, config

def list_all_network_policies():
    # Load Kubernetes configuration, e.g., from ~/.kube/config
    config.load_kube_config()

    # Create an instance of the API class
    k8s_networking_api = client.NetworkingV1Api()

    # List all NetworkPolicies across all namespaces
    all_network_policies = k8s_networking_api.list_network_policy_for_all_namespaces()
    res=set()
    # Filter and print NetworkPolicies
    for np in all_network_policies.items:
        np_name = np.metadata.name
        np_namespace = np.metadata.namespace
        # Assuming the name format is 'allow-from-{namespace_from}-to-{namespace_to}'
        # and trying to extract namespace_from and namespace_to from the name
        if np_name.startswith("allow-from-") and "-to-" in np_name:
            _, namespace_from_part = np_name.split("allow-from-", 1)
            namespace1, namespace2 = namespace_from_part.split("-to-", 1)
            res.add(tuple(sorted((namespace1,namespace2))))
        else:
            # Print other NetworkPolicies that don't follow the naming convention
            # print(f"Other NetworkPolicy Name: {np_name}, Namespace: {np_namespace}")
            pass
    return res
        

# Call the function to list all NetworkPolicies

