// GENERATED CODE -- DO NOT EDIT!

'use strict';
var grpc = require('@grpc/grpc-js');
var run_pb = require('./run_pb.js');

function serialize_RegisterRequest(arg) {
  if (!(arg instanceof run_pb.RegisterRequest)) {
    throw new Error('Expected argument of type RegisterRequest');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_RegisterRequest(buffer_arg) {
  return run_pb.RegisterRequest.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_RegisterResponse(arg) {
  if (!(arg instanceof run_pb.RegisterResponse)) {
    throw new Error('Expected argument of type RegisterResponse');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_RegisterResponse(buffer_arg) {
  return run_pb.RegisterResponse.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_StreamResponse(arg) {
  if (!(arg instanceof run_pb.StreamResponse)) {
    throw new Error('Expected argument of type StreamResponse');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_StreamResponse(buffer_arg) {
  return run_pb.StreamResponse.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_SubscriptionRequest(arg) {
  if (!(arg instanceof run_pb.SubscriptionRequest)) {
    throw new Error('Expected argument of type SubscriptionRequest');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_SubscriptionRequest(buffer_arg) {
  return run_pb.SubscriptionRequest.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_SubscriptionResponse(arg) {
  if (!(arg instanceof run_pb.SubscriptionResponse)) {
    throw new Error('Expected argument of type SubscriptionResponse');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_SubscriptionResponse(buffer_arg) {
  return run_pb.SubscriptionResponse.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_UnregisterRequest(arg) {
  if (!(arg instanceof run_pb.UnregisterRequest)) {
    throw new Error('Expected argument of type UnregisterRequest');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_UnregisterRequest(buffer_arg) {
  return run_pb.UnregisterRequest.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_UnregisterResponse(arg) {
  if (!(arg instanceof run_pb.UnregisterResponse)) {
    throw new Error('Expected argument of type UnregisterResponse');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_UnregisterResponse(buffer_arg) {
  return run_pb.UnregisterResponse.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_UnsubscribeRequest(arg) {
  if (!(arg instanceof run_pb.UnsubscribeRequest)) {
    throw new Error('Expected argument of type UnsubscribeRequest');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_UnsubscribeRequest(buffer_arg) {
  return run_pb.UnsubscribeRequest.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_UnsubscribeResponse(arg) {
  if (!(arg instanceof run_pb.UnsubscribeResponse)) {
    throw new Error('Expected argument of type UnsubscribeResponse');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_UnsubscribeResponse(buffer_arg) {
  return run_pb.UnsubscribeResponse.deserializeBinary(new Uint8Array(buffer_arg));
}


var RunningServiceService = exports.RunningServiceService = {
  register: {
    path: '/RunningService/Register',
    requestStream: false,
    responseStream: false,
    requestType: run_pb.RegisterRequest,
    responseType: run_pb.RegisterResponse,
    requestSerialize: serialize_RegisterRequest,
    requestDeserialize: deserialize_RegisterRequest,
    responseSerialize: serialize_RegisterResponse,
    responseDeserialize: deserialize_RegisterResponse,
  },
  unregister: {
    path: '/RunningService/Unregister',
    requestStream: false,
    responseStream: false,
    requestType: run_pb.UnregisterRequest,
    responseType: run_pb.UnregisterResponse,
    requestSerialize: serialize_UnregisterRequest,
    requestDeserialize: deserialize_UnregisterRequest,
    responseSerialize: serialize_UnregisterResponse,
    responseDeserialize: deserialize_UnregisterResponse,
  },
  subscribe: {
    path: '/RunningService/Subscribe',
    requestStream: false,
    responseStream: false,
    requestType: run_pb.SubscriptionRequest,
    responseType: run_pb.SubscriptionResponse,
    requestSerialize: serialize_SubscriptionRequest,
    requestDeserialize: deserialize_SubscriptionRequest,
    responseSerialize: serialize_SubscriptionResponse,
    responseDeserialize: deserialize_SubscriptionResponse,
  },
  unsubscribe: {
    path: '/RunningService/Unsubscribe',
    requestStream: false,
    responseStream: false,
    requestType: run_pb.UnsubscribeRequest,
    responseType: run_pb.UnsubscribeResponse,
    requestSerialize: serialize_UnsubscribeRequest,
    requestDeserialize: deserialize_UnsubscribeRequest,
    responseSerialize: serialize_UnsubscribeResponse,
    responseDeserialize: deserialize_UnsubscribeResponse,
  },
  eventStream: {
    path: '/RunningService/EventStream',
    requestStream: false,
    responseStream: true,
    requestType: run_pb.RegisterRequest,
    responseType: run_pb.StreamResponse,
    requestSerialize: serialize_RegisterRequest,
    requestDeserialize: deserialize_RegisterRequest,
    responseSerialize: serialize_StreamResponse,
    responseDeserialize: deserialize_StreamResponse,
  },
};

exports.RunningServiceClient = grpc.makeGenericClientConstructor(RunningServiceService, 'RunningService');
