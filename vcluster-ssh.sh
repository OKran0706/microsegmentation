#!/bin/bash

# Exit on any error


# Create Kubernetes namespace
kubectl create namespace vcluster

set -e
# Create a virtual cluster in the 'vcluster' namespace
vcluster create ssh -n vcluster

# Add the securecodebox Helm repository
helm repo add securecodebox https://charts.securecodebox.io/
helm repo update

# Install the dummy SSH server using Helm
helm install my-dummy-ssh securecodebox/dummy-ssh --version 3.14.3 --namespace vcluster
# vcluster disconnect
echo "SSH honeypot deployment completed."
