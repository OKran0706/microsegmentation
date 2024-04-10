from kubernetes import client, config

def create_namespace(api_instance, namespace):
    """Create a namespace."""
    ns = client.V1Namespace(
        metadata=client.V1ObjectMeta(name=namespace)
    )
    api_instance.create_namespace(body=ns)

def create_pod(api_instance, namespace, pod_name, image):
    """Create a pod in the specified namespace."""
    pod_body = client.V1Pod(
        metadata=client.V1ObjectMeta(name=pod_name),
        spec=client.V1PodSpec(
            containers=[client.V1Container(
                name=pod_name,
                image=image,
                command=["sleep", "infinity"]  # Keeps the container running
            )]
        )
    )
    api_instance.create_namespaced_pod(namespace=namespace, body=pod_body)

def main():
    config.load_kube_config()  # Load kubeconfig file
    
    core_v1_api = client.CoreV1Api()

    # Namespace and image details
    setups = [
        {"namespace": "kali-linux", "pod_name": "kali-netcat", "image": "kalilinux/kali-rolling"},
        {"namespace": "ubuntu", "pod_name": "ubuntu-pod", "image": "ubuntu:20.04"}
    ]

    for setup in setups:
        create_namespace(core_v1_api, setup["namespace"])
        create_pod(core_v1_api, setup["namespace"], setup["pod_name"], setup["image"])
        print(f"Created {setup['pod_name']} in {setup['namespace']} namespace.")

if __name__ == "__main__":
    main()
