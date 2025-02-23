# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import project_pb2 as project__pb2


class BankStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.MsgDelivery = channel.unary_unary(
                '/Bank/MsgDelivery',
                request_serializer=project__pb2.MsgDeliveryRequest.SerializeToString,
                response_deserializer=project__pb2.MsgDeliveryResponse.FromString,
                )


class BankServicer(object):
    """Missing associated documentation comment in .proto file."""

    def MsgDelivery(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_BankServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'MsgDelivery': grpc.unary_unary_rpc_method_handler(
                    servicer.MsgDelivery,
                    request_deserializer=project__pb2.MsgDeliveryRequest.FromString,
                    response_serializer=project__pb2.MsgDeliveryResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Bank', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Bank(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def MsgDelivery(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Bank/MsgDelivery',
            project__pb2.MsgDeliveryRequest.SerializeToString,
            project__pb2.MsgDeliveryResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
