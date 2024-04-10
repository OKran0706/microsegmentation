from flask import Flask, request, jsonify
import json
import get_connections
import change_network_policy
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if data["output_fields"]["k8s.pod.name"] is None:
        return jsonify(success=True)

    
    if data and data["priority"] in ("Warning", "Notice", "Critical") and data["output_fields"]["proc.name"]!="cilium-cni":
        print(data["priority"] )
        print("Received webhook data:")
        print(json.dumps(data,indent=4, sort_keys=True))

        if data["output_fields"]["container.id"]!="host" and data["priority"]=="Critical":
            print("namespace",data["output_fields"]["k8s.ns.name"])
        
            choice=input("Enter 1 to isolate namespace: "+ data["output_fields"]["k8s.ns.name"])
            if choice=='1':
                print("Isolating")

                conn=get_connections.list_all_network_policies()

                ns=data["output_fields"]["k8s.ns.name"]
                change_network_policy.default_deny([ns])
                for i in conn:
                    if ns in i:
                        change_network_policy.delete_connection_policy(i[0],i[1])
            else:
                pass
    # Here you can add code to process the data
    return jsonify(success=True)

if __name__ == '__main__':
    app.run(debug=True, port=5000,host='0.0.0.0')
