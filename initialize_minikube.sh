#start
minikube start --driver=docker --network-plugin=cni --cni=false --memory 4096

#install cilium
cilium install --version 1.14.8
cilium hubble enable --ui
cilium status --wait

#install falco
helm install falco falcosecurity/falco   --set driver.kind=modern_ebpf   --set tty=true   --set falcosidekick.enabled=true   --set falcosidekick.config.webhook.address="http://host.minikube.internal:5000/webhook"
helm install kubeshark kubeshark/kubeshark
