import time
import namspace_gen
import deploy_namespaces
from kubernetes import client, config
import pod_gen
import deploy_pods
import change_network_policy
import glob
import subprocess
import get_connections
import psutil
# Configure the client to use the cluster's configuration
config.load_kube_config()
REQUIRED_NAMESPACES={'kube-node-lease','kube-system','kube-public','default'}




def get_namespaces():
    v1 = client.CoreV1Api()
    namespaces = set()
    for ns in v1.list_namespace().items:
        namespaces.add(ns.metadata.name)
    return namespaces


# def list_pods(namespace='default'):
#             #   config.load_kube_config()
#               v1=client.CoreV1Api()
#               print(f"Listing pods in namespace {namespace}")
#               pods=v1.list_namespaced_pod(namespace)
#               res=set()
#               for pod in pods.items:
#                    res.add(pod.metadata.name)
#               return res

def list_pods(namespace='default'):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    print(f"Listing pods in namespace {namespace}")
    pods = v1.list_namespaced_pod(namespace)
    res = set()
    for pod in pods.items:
        # Check if the deletion_timestamp is None (pod is not being terminated)
        if pod.metadata.deletion_timestamp is None:
            res.add(pod.metadata.name)
    return res

def delete_all_namespaces(exclude=['default', 'kube-system', 'kube-public', 'kube-node-lease']):
    v1 = client.CoreV1Api()
    # Fetch all namespaces
    namespaces = v1.list_namespace()
    flag=0
    
    for ns in namespaces.items:
        # Check if the namespace is not in the exclude list
        if ns.metadata.name not in exclude:
            try:
                print(f"Deleting namespace: {ns.metadata.name}")
                # Delete namespace
                v1.delete_namespace(ns.metadata.name)
            except Exception as e:
                print(f"Failed to delete namespace {ns.metadata.name}: {e}")
                flag=1
    print("Namespace deletion request completed.")
    return flag

choice=None
while choice != 11:
    options= ['Add namespaces', 'Add pods', 'Display Namespaces', 'Display pods','Change Network Policy', 'Generate Network Graph','Start Network Monitoring','Isolate a Namespace','Cleanup','Scan Conatiner Image']
    for num, string in enumerate(options):
        print(num+1 ,': '+string)
    choice = int(input('Enter your choice - \n'))
    # print(choice)

    if choice == 1:
        #Add namespaces
        namespaces= set(map(lambda x: x.lower(),input('Enter comma separated names of namespaces you want to add:\n').split(',')))
        existing_namespaces=get_namespaces()
        # namespaces={'hello','hi','by'}
        # existing_namespaces={'hello','hie','bye','hi'}
        res=namespaces-existing_namespaces
        namspace_gen.generate_and_save_namespaces(res)
        deploy_namespaces.deploy_namespace_yaml('namespaces',res)
        print("Adding default deny policies")
        change_network_policy.default_deny(res)
        
        




        if len(res)!=len(namespaces):
            print('Remaining namespaces already existed')
        
    elif choice == 2:
        pods= set(input('Enter comma separated names of pods you want to add:\n').split(','))
        print('Available namespaces:')
        namespaces=get_namespaces()-REQUIRED_NAMESPACES
        for j in namespaces:
            print(j)
        ns=input('Enter the namespace: ').lower()
        
        if ns not in get_namespaces():
             print(f"Namespace {ns} does not exist")
             continue
        existing_pods=list_pods(ns)
        new_pods=pods-existing_pods
        try:
            pod_gen.generate_and_save_pods(new_pods,ns)
        except Exception as e:
            print('Error occured')
        
        print(new_pods)
        
        deploy_pods.deploy_pod_yaml('output_pods',new_pods,ns)
        
         
         
    elif choice == 3:
        namespaces=get_namespaces()
        for i in namespaces:
            print(i)


    elif choice == 4:
         
         print('Available namespaces:')
         namespaces=get_namespaces()
         for j in namespaces:
              print(j)
         ns=input("Enter namespace you want the pods for: ")
         if ns not in namespaces:
              print(f"Namespace {ns} does not exist")
              continue
         pods=list_pods(ns)
         for i in pods:
              print(i)
    elif choice == 5: #Change network policy
        print("Available Choices:")
        opt=['Add Connection','Delete Connection','Add necessary Connections']
        for i,j in enumerate(opt):
            print(i+1,j)
        choice_1=input("Choose 1 option:")
        if choice_1=='1':
            print('Available namespaces:')
            namespaces=get_namespaces()
            for j in namespaces:
                print(j)
            namespaces=input('Enter comma separated value of 2 namespaces you want to connect: ').split(',')
            change_network_policy.add_connection_and_apply(namespaces[0].lower(),namespaces[1].lower())
        elif choice_1 == '2':
            print('Available Connections:')
            import get_connections
            connections= get_connections.list_all_network_policies()
            for ns1,ns2 in connections:
                print(ns1," <> ",ns2)
            namespaces=input('\nEnter comma separated value of 2 namespaces you want to disconnect: ').split(',')
            change_network_policy.delete_connection_policy(namespaces[0].lower(),namespaces[1].lower())
        
        elif choice_1 == '3':
            print('Available namespaces:')
            namespaces=get_namespaces()
            for j in namespaces:
                print(j)
            namespace=input('Enter namespace you want to connect: ')
            change_network_policy.add_connection_to_necessary_namespaces(namespace)
            
        else:
            print('Invalid Option')
    elif choice == 6:
        import view
        view.plot_ns_graph()
    
    elif choice == 7:
        nm_choices=['hubble','kubeshark']
        for i,j in enumerate(nm_choices):
            print(i+1,j)
        sub_choice= input('Enter a choice')
        if sub_choice=='1':
            def kill_process_using_port(port):
                command = f"lsof -ti:{port}"
                try:
                    result = subprocess.run(command, shell=True, check=True, text=True, stdout=subprocess.PIPE)
                    pid = result.stdout.strip()
                    return pid
                except subprocess.CalledProcessError:
                    return None
            


            try:
                # Use subprocess.Popen for non-blocking execution
                res=kill_process_using_port(12000)
                if res != None:
                    print(f"Port 12000 already in use by Processes with pids: \n{res}\nTry sudo kill {res}")
                    break

                subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', 'cilium hubble ui'])

            except subprocess.SubprocessError as e:
                print(f"Failed to execute command: {e}")
        elif sub_choice=='2':
            try:
                # Use subprocess.Popen for non-blocking execution
                # res=kill_process_using_port(12000)
                # if res != None:
                #     print(f"Port 12000 already in use by Processes with pids: \n{res}\nTry sudo kill {res}")
                #     break

                subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', ' xdg-open http://localhost:8899; kubectl port-forward service/kubeshark-front 8899:80'])
                # subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', 'xdg-open http://localhost:8899'])


            except subprocess.SubprocessError as e:
                print(f"Failed to execute command: {e}")

    elif choice == 8:
        print('Available namespaces:')
        namespaces=get_namespaces()
        for j in namespaces:
            print(j)
        ns=input("Enter the namespace you want to isolate: ").strip().lower()
        change_network_policy.default_deny([ns])
        conn=get_connections.list_all_network_policies()
        for i in conn:
            if ns in i:
                change_network_policy.delete_connection_policy(i[0],i[1])
                


    elif choice == 7:
        import view
        view.plot_ns_graph()
        

    elif choice == 9:
        import delete_yaml_files
        res=delete_all_namespaces()
        delete_yaml_files.delete_all_yaml_files('output_pods')
        delete_yaml_files.delete_all_yaml_files('namespaces')
        delete_yaml_files.delete_all_yaml_files('policies')
        if res == 1:
            print("Error occurred in deleting some namespaces")
    
    elif choice == 10:
        img=input("Enter image name and tag (optional) \n Image:Tag -->  ")
        import grype_scan
        grype_scan.scan_image_with_grype(img)