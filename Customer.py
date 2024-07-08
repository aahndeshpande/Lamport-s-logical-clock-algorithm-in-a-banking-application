import time
import sys
import json
import os

import grpc
from matplotlib.font_manager import json_dump
import project_pb2
import project_pb2_grpc


class Customer:
    def __init__(self, id, events):
        self.id = id
        self.events = events
        self.recvMsg = list()
        self.channel = None
        self.stub = None
        self.port = 50051 + id
        self.lastProcessedId = -1
        self.logical_clock = 0
        self.result_checker = {} 

    def appendEvents(self, events):
        self.events.extend(events)

    def createStub(self):
        self.channel = grpc.insecure_channel(f"localhost:{self.port}")
        stub = project_pb2_grpc.BankStub(self.channel)
        return stub

    def executeEvents(self):
        if self.stub is None:
            self.stub = self.createStub()
        result = {
            "id": self.id,
            "type": "customer",
            "events": [],
        }
        
         
        for i in range(self.lastProcessedId + 1, len(self.events)):
            self.logical_clock += 1
            self.lastProcessedId = i

            if self.events[i]["interface"] == "deposit":
                response = self.stub.MsgDelivery(project_pb2.MsgDeliveryRequest(
                    id=self.id, event_id=self.events[i]["customer-request-id"], interface="deposit",
                    money=self.events[i]["money"], logical_clock=self.logical_clock))
                result["events"].append({
                    "customer-request-id": self.events[i]["customer-request-id"],
                    "logical_clock": self.logical_clock,
                    "interface": self.events[i]["interface"],
                    "comment": "event_sent from customer " + str(self.id)
                })
                self.result_checker = {
                    "id": self.id,
                    "type": "customer",
                    "customer-request-id": self.events[i]["customer-request-id"],
                    "logical_clock": self.logical_clock,
                    "interface": self.events[i]["interface"],
                    "comment": "event_sent from customer " + str(self.id)
                   
                }
                
                output_path = os.path.join("output", "output3.json")
                with open(output_path, 'a') as json_file:
                    json.dump(self.result_checker, json_file, indent=2)
                    json_file.write(",")
                    

            elif self.events[i]["interface"] == "query":
                response = self.stub.MsgDelivery(project_pb2.MsgDeliveryRequest(
                    id=self.id, event_id=self.events[i]["customer-request-id"], interface="query",
                    logical_clock=self.logical_clock))  
                result["events"].append({
                    "customer-request-id": self.events[i]["customer-request-id"],
                    "logical_clock": self.logical_clock,  
                    "interface": self.events[i]["interface"],
                    "comment": "event_sent from customer " + str(self.id)
                })
                
                
            elif self.events[i]["interface"] == "withdraw":
                response = self.stub.MsgDelivery(project_pb2.MsgDeliveryRequest(
                    id=self.id, event_id=self.events[i]["customer-request-id"], money=self.events[i]["money"],
                    interface="withdraw", logical_clock=self.logical_clock))
                result["events"].append({
                    "customer-request-id": self.events[i]["customer-request-id"],
                    "logical_clock": self.logical_clock,
                    "interface": self.events[i]["interface"],
                    "comment": "event_sent from customer " + str(self.id)
                })
                self.result_checker ={
                    "id": self.id,
                    "type": "customer",
                    "customer-request-id": self.events[i]["customer-request-id"],
                    "logical_clock": self.logical_clock,
                    "interface": self.events[i]["interface"],
                    "comment": "event_sent from customer " + str(self.id)
                }
                #output3
                output_path = os.path.join("output", "output3.json")
                with open(output_path, 'a') as json_file:
                    json.dump(self.result_checker, json_file, indent=2)
                    if(int(self.id)!=10):
                        json_file.write(",")
                
                

        return result


if __name__ == '__main__':
    file_path = f'{sys.argv[1]}'
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)

    customerData = []
    customers = {}
    response = []
    
    for i in range(len(data)):
        if data[i]["type"] == "customer":
            if data[i]["id"] not in customers:
                customers[data[i]["id"]] = Customer(
                    data[i]["id"], data[i]["customer-requests"])
                response.append(customers[data[i]["id"]].executeEvents())
             
                
                
            else:
                
                customers[data[i]["id"]].appendEvents(data[i]["customer-requests"])
                response.append(customers[data[i]["id"]].executeEvents())
                
    output_path1 = os.path.join("output", "output3.json")         
    with open(output_path1, 'a') as json_file:
                    json_file.write("]")
        
        
    print(response)

    # Write result_checker to "output3.json"
    output_path = os.path.join("output", "output1.json")
    with open(output_path, 'w') as json_file:
        json.dump(response, json_file, indent=2)
