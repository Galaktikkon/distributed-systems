// package: 
// file: run.proto

/* tslint:disable */
/* eslint-disable */

import * as grpc from "@grpc/grpc-js";
import * as run_pb from "./run_pb";

interface IRunningServiceService extends grpc.ServiceDefinition<grpc.UntypedServiceImplementation> {
    register: IRunningServiceService_IRegister;
    unregister: IRunningServiceService_IUnregister;
    subscribe: IRunningServiceService_ISubscribe;
    unsubscribe: IRunningServiceService_IUnsubscribe;
    eventStream: IRunningServiceService_IEventStream;
}

interface IRunningServiceService_IRegister extends grpc.MethodDefinition<run_pb.RegisterRequest, run_pb.RegisterResponse> {
    path: "/RunningService/Register";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<run_pb.RegisterRequest>;
    requestDeserialize: grpc.deserialize<run_pb.RegisterRequest>;
    responseSerialize: grpc.serialize<run_pb.RegisterResponse>;
    responseDeserialize: grpc.deserialize<run_pb.RegisterResponse>;
}
interface IRunningServiceService_IUnregister extends grpc.MethodDefinition<run_pb.UnregisterRequest, run_pb.UnregisterResponse> {
    path: "/RunningService/Unregister";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<run_pb.UnregisterRequest>;
    requestDeserialize: grpc.deserialize<run_pb.UnregisterRequest>;
    responseSerialize: grpc.serialize<run_pb.UnregisterResponse>;
    responseDeserialize: grpc.deserialize<run_pb.UnregisterResponse>;
}
interface IRunningServiceService_ISubscribe extends grpc.MethodDefinition<run_pb.SubscriptionRequest, run_pb.SubscriptionResponse> {
    path: "/RunningService/Subscribe";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<run_pb.SubscriptionRequest>;
    requestDeserialize: grpc.deserialize<run_pb.SubscriptionRequest>;
    responseSerialize: grpc.serialize<run_pb.SubscriptionResponse>;
    responseDeserialize: grpc.deserialize<run_pb.SubscriptionResponse>;
}
interface IRunningServiceService_IUnsubscribe extends grpc.MethodDefinition<run_pb.UnsubscribeRequest, run_pb.UnsubscribeResponse> {
    path: "/RunningService/Unsubscribe";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<run_pb.UnsubscribeRequest>;
    requestDeserialize: grpc.deserialize<run_pb.UnsubscribeRequest>;
    responseSerialize: grpc.serialize<run_pb.UnsubscribeResponse>;
    responseDeserialize: grpc.deserialize<run_pb.UnsubscribeResponse>;
}
interface IRunningServiceService_IEventStream extends grpc.MethodDefinition<run_pb.RegisterRequest, run_pb.StreamResponse> {
    path: "/RunningService/EventStream";
    requestStream: false;
    responseStream: true;
    requestSerialize: grpc.serialize<run_pb.RegisterRequest>;
    requestDeserialize: grpc.deserialize<run_pb.RegisterRequest>;
    responseSerialize: grpc.serialize<run_pb.StreamResponse>;
    responseDeserialize: grpc.deserialize<run_pb.StreamResponse>;
}

export const RunningServiceService: IRunningServiceService;

export interface IRunningServiceServer extends grpc.UntypedServiceImplementation {
    register: grpc.handleUnaryCall<run_pb.RegisterRequest, run_pb.RegisterResponse>;
    unregister: grpc.handleUnaryCall<run_pb.UnregisterRequest, run_pb.UnregisterResponse>;
    subscribe: grpc.handleUnaryCall<run_pb.SubscriptionRequest, run_pb.SubscriptionResponse>;
    unsubscribe: grpc.handleUnaryCall<run_pb.UnsubscribeRequest, run_pb.UnsubscribeResponse>;
    eventStream: grpc.handleServerStreamingCall<run_pb.RegisterRequest, run_pb.StreamResponse>;
}

export interface IRunningServiceClient {
    register(request: run_pb.RegisterRequest, callback: (error: grpc.ServiceError | null, response: run_pb.RegisterResponse) => void): grpc.ClientUnaryCall;
    register(request: run_pb.RegisterRequest, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: run_pb.RegisterResponse) => void): grpc.ClientUnaryCall;
    register(request: run_pb.RegisterRequest, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: run_pb.RegisterResponse) => void): grpc.ClientUnaryCall;
    unregister(request: run_pb.UnregisterRequest, callback: (error: grpc.ServiceError | null, response: run_pb.UnregisterResponse) => void): grpc.ClientUnaryCall;
    unregister(request: run_pb.UnregisterRequest, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: run_pb.UnregisterResponse) => void): grpc.ClientUnaryCall;
    unregister(request: run_pb.UnregisterRequest, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: run_pb.UnregisterResponse) => void): grpc.ClientUnaryCall;
    subscribe(request: run_pb.SubscriptionRequest, callback: (error: grpc.ServiceError | null, response: run_pb.SubscriptionResponse) => void): grpc.ClientUnaryCall;
    subscribe(request: run_pb.SubscriptionRequest, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: run_pb.SubscriptionResponse) => void): grpc.ClientUnaryCall;
    subscribe(request: run_pb.SubscriptionRequest, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: run_pb.SubscriptionResponse) => void): grpc.ClientUnaryCall;
    unsubscribe(request: run_pb.UnsubscribeRequest, callback: (error: grpc.ServiceError | null, response: run_pb.UnsubscribeResponse) => void): grpc.ClientUnaryCall;
    unsubscribe(request: run_pb.UnsubscribeRequest, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: run_pb.UnsubscribeResponse) => void): grpc.ClientUnaryCall;
    unsubscribe(request: run_pb.UnsubscribeRequest, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: run_pb.UnsubscribeResponse) => void): grpc.ClientUnaryCall;
    eventStream(request: run_pb.RegisterRequest, options?: Partial<grpc.CallOptions>): grpc.ClientReadableStream<run_pb.StreamResponse>;
    eventStream(request: run_pb.RegisterRequest, metadata?: grpc.Metadata, options?: Partial<grpc.CallOptions>): grpc.ClientReadableStream<run_pb.StreamResponse>;
}

export class RunningServiceClient extends grpc.Client implements IRunningServiceClient {
    constructor(address: string, credentials: grpc.ChannelCredentials, options?: Partial<grpc.ClientOptions>);
    public register(request: run_pb.RegisterRequest, callback: (error: grpc.ServiceError | null, response: run_pb.RegisterResponse) => void): grpc.ClientUnaryCall;
    public register(request: run_pb.RegisterRequest, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: run_pb.RegisterResponse) => void): grpc.ClientUnaryCall;
    public register(request: run_pb.RegisterRequest, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: run_pb.RegisterResponse) => void): grpc.ClientUnaryCall;
    public unregister(request: run_pb.UnregisterRequest, callback: (error: grpc.ServiceError | null, response: run_pb.UnregisterResponse) => void): grpc.ClientUnaryCall;
    public unregister(request: run_pb.UnregisterRequest, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: run_pb.UnregisterResponse) => void): grpc.ClientUnaryCall;
    public unregister(request: run_pb.UnregisterRequest, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: run_pb.UnregisterResponse) => void): grpc.ClientUnaryCall;
    public subscribe(request: run_pb.SubscriptionRequest, callback: (error: grpc.ServiceError | null, response: run_pb.SubscriptionResponse) => void): grpc.ClientUnaryCall;
    public subscribe(request: run_pb.SubscriptionRequest, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: run_pb.SubscriptionResponse) => void): grpc.ClientUnaryCall;
    public subscribe(request: run_pb.SubscriptionRequest, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: run_pb.SubscriptionResponse) => void): grpc.ClientUnaryCall;
    public unsubscribe(request: run_pb.UnsubscribeRequest, callback: (error: grpc.ServiceError | null, response: run_pb.UnsubscribeResponse) => void): grpc.ClientUnaryCall;
    public unsubscribe(request: run_pb.UnsubscribeRequest, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: run_pb.UnsubscribeResponse) => void): grpc.ClientUnaryCall;
    public unsubscribe(request: run_pb.UnsubscribeRequest, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: run_pb.UnsubscribeResponse) => void): grpc.ClientUnaryCall;
    public eventStream(request: run_pb.RegisterRequest, options?: Partial<grpc.CallOptions>): grpc.ClientReadableStream<run_pb.StreamResponse>;
    public eventStream(request: run_pb.RegisterRequest, metadata?: grpc.Metadata, options?: Partial<grpc.CallOptions>): grpc.ClientReadableStream<run_pb.StreamResponse>;
}
