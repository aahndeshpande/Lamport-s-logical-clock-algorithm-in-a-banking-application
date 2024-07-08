from concurrent import futures
import sys
import json
import grpc
import project_pb2
import project_pb2_grpc
import os

class Branch(project_pb2_grpc.BankServicer):
    def __init__(self, id, balance, branches):
        self.id = id
        self.balance = balance
        self.branches = branches
        self.channelList = list()
        self.stubList = list()
        self.recvMsg = list()
        self.logical_clock = 0  #initialise logical clock 
        self.result_checker= {}
        self.responses = []
        self.branch_events = []  

    def Deposit(self, request):  
        self.balance += request.money
        self.logical_clock = max(self.logical_clock, request.logical_clock) + 1 #event recieved so update logical clock 
        c=0
        self.branch_events.append({
            "customer-request-id": request.event_id,
            "logical_clock": self.logical_clock,
            "interface": request.interface,
            "comment": "event_recv from customer " + str(self.id)
        })
        #for ouput3
        self.result_checker = {
            "id": self.id,
            "customer-request-id": request.event_id,
            "type": "branch",
            "logical_clock": self.logical_clock,
            "interface": request.interface,
            "comment": "event_recv from customer " + str(self.id)
       } 
        output_path3 = os.path.join("output", "output3.json")
        with open(output_path3, 'a') as json_file:
                    json.dump(self.result_checker, json_file, indent=2)
                    json_file.write(",")
        
       
        if len(self.channelList) == 0:
            for id in self.branches:
                if(id!=self.id):
                    
                    port = 50051 + id
                    channel = grpc.insecure_channel(f"localhost:{port}")
                    self.channelList.append(channel)
                    stub = project_pb2_grpc.BankStub(channel)
                    self.stubList.append(stub)

        for stub in self.stubList:
            self.logical_clock +=1 #event sent
            c +=1
            self.branch_events.append({
                
                "customer-request-id": request.event_id,
                "logical_clock": self.logical_clock,
                "interface": "propagate_deposit",
                "comment": "event_sent to branch " + str(c)
        })
            #for ouput3
            self.result_checker = {
            "id": self.id,
            "customer-request-id": request.event_id,
            "type": "branch",
            "logical_clock": self.logical_clock,
            "interface": request.interface,
            "comment": "event_recv from customer " + str(self.id)
       } 
            output_path3 = os.path.join("output", "output3.json")
            with open(output_path3, 'a') as json_file:
                    json.dump(self.result_checker, json_file, indent=2)
                    json_file.write(",")
            stub.MsgDelivery(
                project_pb2.MsgDeliveryRequest(event_id=request.event_id,balance=self.balance,bank_id=self.id, interface="propagate_deposit",
                                               logical_clock=self.logical_clock))

    def Query(self, request):
        self.logical_clock = max(self.logical_clock, request.logical_clock) + 1 #event received 
        
        # Append event data to the branch_events list
        self.branch_events.append({
            "customer-request-id": request.event_id,
            "logical_clock": self.logical_clock,
            "interface": request.interface,
            "comment": "event_recv from branch " + str(self.id)
        })
        #for ouput3
        self.result_checker = {
            "id": self.id,
            "customer-request-id": request.event_id,
            "type": "branch",
            "logical_clock": self.logical_clock,
            "interface": request.interface,
            "comment": "event_recv from customer " + str(self.id)
       } 
        output_path3 = os.path.join("output", "output3.json")
        with open(output_path3, 'a') as json_file:
                    json.dump(self.result_checker, json_file, indent=2)
                    json_file.write(",")


    def Withdraw(self, request):
        
        

        if self.balance >= request.money:
            self.logical_clock=max(self.logical_clock,request.logical_clock)+1 #event received
            k=0
            self.branch_events.append({
            "customer-request-id": request.event_id,
            "logical_clock": self.logical_clock,
            "interface": request.interface,
            "comment": "event_recv from customer " + str(self.id)
        })
            #for ouput3
            self.result_checker = {
                        "id": self.id,
                        "customer-request-id": request.event_id,
                        "type": "branch",
                        "logical_clock": self.logical_clock,
                        "interface": request.interface,
                        "comment": "event_recv from customer " + str(self.id)
                } 
            output_path3 = os.path.join("output", "output3.json")
            with open(output_path3, 'a') as json_file:
                    json.dump(self.result_checker, json_file, indent=2)
                    json_file.write(",")
           
            self.balance -= request.money

            if len(self.channelList) == 0:
                for id in self.branches:
                    if(id!=self.id):
                        
                        port = 50051 + id
                        channel = grpc.insecure_channel(f"localhost:{port}")
                        self.channelList.append(channel)
                        stub = project_pb2_grpc.BankStub(channel)
                        self.stubList.append(stub)

            for stub in self.stubList:
                
                k +=1 
                
                self.logical_clock +=1  #event sent
                self.branch_events.append({
                
                "customer-request-id": request.event_id,
                "logical_clock": self.logical_clock,
                "interface": "propagate_withdraw",
                "comment": "event_sent to branch " + str(k)
        })       
                #for ouput3
                self.result_checker = {
                                        "id": self.id,
                                        "customer-request-id": request.event_id,
                                        "type": "branch",
                                        "logical_clock": self.logical_clock,
                                        "interface": request.interface,
                                        "comment": "event_recv from customer " + str(self.id)
                                } 
                output_path3 = os.path.join("output", "output3.json")
                with open(output_path3, 'a') as json_file:
                    json.dump(self.result_checker, json_file, indent=2)
                    json_file.write(",")
                stub.MsgDelivery(
                    project_pb2.MsgDeliveryRequest(event_id=request.event_id,bank_id=self.id, balance=self.balance, interface="propagate_withdraw",
                                                   logical_clock=self.logical_clock))

    def Propagate_Deposit(self, request):
        self.balance = request.balance
        self.logical_clock = max(self.logical_clock,request.logical_clock)+1 #propagate so event recv
        self.branch_events.append( {
            "customer-request-id": request.event_id,
            "logical_clock": self.logical_clock,
            "interface": request.interface,
            "comment": "event_recv from branch " + str(request.bank_id)
        })
        #for ouput3
        self.result_checker = {
            "id": self.id,
            "customer-request-id": request.event_id,
            "type": "branch",
            "logical_clock": self.logical_clock,
            "interface": request.interface,
            "comment": "event_recv from customer " + str(self.id)
       } 
        output_path3 = os.path.join("output", "output3.json")
        with open(output_path3, 'a') as json_file:
                    json.dump(self.result_checker, json_file, indent=2)
                    json_file.write(",")

    def Propagate_Withdraw(self, request):
        self.logical_clock = max(self.logical_clock,request.logical_clock)+1
        self.balance = request.balance
        self.branch_events.append( {
            "customer-request-id": request.event_id,
            "logical_clock": self.logical_clock,
            "interface": request.interface,
            "comment": "event_recv from branch " + str(request.bank_id)
        })
        #for ouput3
        self.result_checker ={
            "id": self.id,
            "customer-request-id": request.event_id,
            "type": "branch",
            "logical_clock": self.logical_clock,
            "interface": request.interface,
            "comment": "event_recv from customer " + str(self.id)
       } 
        output_path3 = os.path.join("output", "output3.json")
        with open(output_path3, 'a') as json_file:
                    json.dump(self.result_checker, json_file,indent=2)
                    json_file.write(",")
                
        
    def executeEvents(self):
        
        result = {
            "id": self.id,
            "type": "branch",
            "events": self.branch_events,
            
        }
        
            
            
        return result

    def MsgDelivery(self, request, context):
        

        self.recvMsg.append(request)
                 
        if request.interface == "query":  
            self.Query(request=request)
        elif request.interface == "deposit": 
            self.Deposit(request=request)
        elif request.interface == "withdraw": 
            self.Withdraw(request=request)
        elif request.interface == "propagate_withdraw":
            self.Propagate_Withdraw(request=request)
        elif request.interface == "propagate_deposit":
            self.Propagate_Deposit(request=request)
        
        # returning msg delivery response
        return project_pb2.MsgDeliveryResponse(
            id=self.id,
            event_id=request.event_id,
            balance=self.balance,
            result=None,  
            logical_clock= self.logical_clock
        )

def start_grpc_servers(branches):
    servers = []
    branch_instances = []  # List to store instances of Branch

    try:
        for branch_data in branches:
            server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
            branch = Branch(id=branch_data["id"],
                            balance=branch_data["balance"], branches=[b["id"] for b in branches])
            project_pb2_grpc.add_BankServicer_to_server(branch, server)
            port = 50051 + branch_data["id"]
            server.add_insecure_port(f'[::]:{port}')
            server.start()
            print(f"Branch {branch_data['id']} started on port: {port}")
            servers.append(server)
            branch_instances.append(branch)

        for server in servers:
            server.wait_for_termination()

    except KeyboardInterrupt:
        print("\nStopping all servers.")
        for server in servers:
            server.stop(grace=None)  # Graceful shutdown
        for server in servers:
            server.wait_for_termination()

    return branch_instances

def load_json_file(file_path):
            
            try:
                with open(file_path, 'r') as json_file:
                    
                    data = json.load(json_file)
                    return data
            except json.JSONDecodeError:
                        print(f"Error decoding JSON in file: {file_path}")
                        return None

if __name__ == '__main__':
    file_path = f'{sys.argv[1]}'
    data = load_json_file(file_path)
    
    output_path_checker3 = os.path.join("output", "output3.json")
    with open(output_path_checker3, 'a') as json_file:
                json_file.write("[")
                
    if data is not None:
        branches = [branch for branch in data if branch.get("type") == "branch"]

        branch_instances = start_grpc_servers(branches)  # Retrieve the list of Branch instances
#output 2 
    if branch_instances:
        output_path = os.path.join("output", "output2.json")
  
        combined_results = []
      

        for branch in branch_instances:
            branch_results = branch.executeEvents()
            combined_results.append(branch_results)
            

        with open(output_path, 'w') as json_file:
            json.dump(combined_results, json_file, indent=2)
