// package: 
// file: run.proto

/* tslint:disable */
/* eslint-disable */

import * as jspb from "google-protobuf";

export class RunningEvent extends jspb.Message { 
    getId(): number;
    setId(value: number): RunningEvent;
    getCity(): string;
    setCity(value: string): RunningEvent;
    getWeather(): WeatherCondition;
    setWeather(value: WeatherCondition): RunningEvent;
    getDistance(): DistanceType;
    setDistance(value: DistanceType): RunningEvent;
    getStartTime(): string;
    setStartTime(value: string): RunningEvent;
    clearTagsList(): void;
    getTagsList(): Array<string>;
    setTagsList(value: Array<string>): RunningEvent;
    addTags(value: string, index?: number): string;

    serializeBinary(): Uint8Array;
    toObject(includeInstance?: boolean): RunningEvent.AsObject;
    static toObject(includeInstance: boolean, msg: RunningEvent): RunningEvent.AsObject;
    static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
    static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
    static serializeBinaryToWriter(message: RunningEvent, writer: jspb.BinaryWriter): void;
    static deserializeBinary(bytes: Uint8Array): RunningEvent;
    static deserializeBinaryFromReader(message: RunningEvent, reader: jspb.BinaryReader): RunningEvent;
}

export namespace RunningEvent {
    export type AsObject = {
        id: number,
        city: string,
        weather: WeatherCondition,
        distance: DistanceType,
        startTime: string,
        tagsList: Array<string>,
    }
}

export class SubscriptionRequest extends jspb.Message { 
    getClientId(): string;
    setClientId(value: string): SubscriptionRequest;
    clearCitiesList(): void;
    getCitiesList(): Array<string>;
    setCitiesList(value: Array<string>): SubscriptionRequest;
    addCities(value: string, index?: number): string;
    clearDistancesList(): void;
    getDistancesList(): Array<DistanceType>;
    setDistancesList(value: Array<DistanceType>): SubscriptionRequest;
    addDistances(value: DistanceType, index?: number): DistanceType;
    clearTagsList(): void;
    getTagsList(): Array<string>;
    setTagsList(value: Array<string>): SubscriptionRequest;
    addTags(value: string, index?: number): string;
    clearWeatherConditionsList(): void;
    getWeatherConditionsList(): Array<WeatherCondition>;
    setWeatherConditionsList(value: Array<WeatherCondition>): SubscriptionRequest;
    addWeatherConditions(value: WeatherCondition, index?: number): WeatherCondition;

    serializeBinary(): Uint8Array;
    toObject(includeInstance?: boolean): SubscriptionRequest.AsObject;
    static toObject(includeInstance: boolean, msg: SubscriptionRequest): SubscriptionRequest.AsObject;
    static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
    static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
    static serializeBinaryToWriter(message: SubscriptionRequest, writer: jspb.BinaryWriter): void;
    static deserializeBinary(bytes: Uint8Array): SubscriptionRequest;
    static deserializeBinaryFromReader(message: SubscriptionRequest, reader: jspb.BinaryReader): SubscriptionRequest;
}

export namespace SubscriptionRequest {
    export type AsObject = {
        clientId: string,
        citiesList: Array<string>,
        distancesList: Array<DistanceType>,
        tagsList: Array<string>,
        weatherConditionsList: Array<WeatherCondition>,
    }
}

export class SubscriptionResponse extends jspb.Message { 
    getSubscriptionId(): number;
    setSubscriptionId(value: number): SubscriptionResponse;
    getMessage(): string;
    setMessage(value: string): SubscriptionResponse;
    getSuccess(): boolean;
    setSuccess(value: boolean): SubscriptionResponse;

    serializeBinary(): Uint8Array;
    toObject(includeInstance?: boolean): SubscriptionResponse.AsObject;
    static toObject(includeInstance: boolean, msg: SubscriptionResponse): SubscriptionResponse.AsObject;
    static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
    static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
    static serializeBinaryToWriter(message: SubscriptionResponse, writer: jspb.BinaryWriter): void;
    static deserializeBinary(bytes: Uint8Array): SubscriptionResponse;
    static deserializeBinaryFromReader(message: SubscriptionResponse, reader: jspb.BinaryReader): SubscriptionResponse;
}

export namespace SubscriptionResponse {
    export type AsObject = {
        subscriptionId: number,
        message: string,
        success: boolean,
    }
}

export class UnsubscribeRequest extends jspb.Message { 
    getClientId(): string;
    setClientId(value: string): UnsubscribeRequest;
    getSubscriptionId(): number;
    setSubscriptionId(value: number): UnsubscribeRequest;

    serializeBinary(): Uint8Array;
    toObject(includeInstance?: boolean): UnsubscribeRequest.AsObject;
    static toObject(includeInstance: boolean, msg: UnsubscribeRequest): UnsubscribeRequest.AsObject;
    static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
    static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
    static serializeBinaryToWriter(message: UnsubscribeRequest, writer: jspb.BinaryWriter): void;
    static deserializeBinary(bytes: Uint8Array): UnsubscribeRequest;
    static deserializeBinaryFromReader(message: UnsubscribeRequest, reader: jspb.BinaryReader): UnsubscribeRequest;
}

export namespace UnsubscribeRequest {
    export type AsObject = {
        clientId: string,
        subscriptionId: number,
    }
}

export class UnsubscribeResponse extends jspb.Message { 
    getSuccess(): boolean;
    setSuccess(value: boolean): UnsubscribeResponse;
    getMessage(): string;
    setMessage(value: string): UnsubscribeResponse;

    serializeBinary(): Uint8Array;
    toObject(includeInstance?: boolean): UnsubscribeResponse.AsObject;
    static toObject(includeInstance: boolean, msg: UnsubscribeResponse): UnsubscribeResponse.AsObject;
    static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
    static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
    static serializeBinaryToWriter(message: UnsubscribeResponse, writer: jspb.BinaryWriter): void;
    static deserializeBinary(bytes: Uint8Array): UnsubscribeResponse;
    static deserializeBinaryFromReader(message: UnsubscribeResponse, reader: jspb.BinaryReader): UnsubscribeResponse;
}

export namespace UnsubscribeResponse {
    export type AsObject = {
        success: boolean,
        message: string,
    }
}

export class ErrorResponse extends jspb.Message { 
    getErrorMessage(): string;
    setErrorMessage(value: string): ErrorResponse;

    serializeBinary(): Uint8Array;
    toObject(includeInstance?: boolean): ErrorResponse.AsObject;
    static toObject(includeInstance: boolean, msg: ErrorResponse): ErrorResponse.AsObject;
    static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
    static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
    static serializeBinaryToWriter(message: ErrorResponse, writer: jspb.BinaryWriter): void;
    static deserializeBinary(bytes: Uint8Array): ErrorResponse;
    static deserializeBinaryFromReader(message: ErrorResponse, reader: jspb.BinaryReader): ErrorResponse;
}

export namespace ErrorResponse {
    export type AsObject = {
        errorMessage: string,
    }
}

export class BufferedEventInfo extends jspb.Message { 
    getBufferedCount(): number;
    setBufferedCount(value: number): BufferedEventInfo;

    serializeBinary(): Uint8Array;
    toObject(includeInstance?: boolean): BufferedEventInfo.AsObject;
    static toObject(includeInstance: boolean, msg: BufferedEventInfo): BufferedEventInfo.AsObject;
    static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
    static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
    static serializeBinaryToWriter(message: BufferedEventInfo, writer: jspb.BinaryWriter): void;
    static deserializeBinary(bytes: Uint8Array): BufferedEventInfo;
    static deserializeBinaryFromReader(message: BufferedEventInfo, reader: jspb.BinaryReader): BufferedEventInfo;
}

export namespace BufferedEventInfo {
    export type AsObject = {
        bufferedCount: number,
    }
}

export class StreamResponse extends jspb.Message { 

    hasEvent(): boolean;
    clearEvent(): void;
    getEvent(): RunningEvent | undefined;
    setEvent(value?: RunningEvent): StreamResponse;

    hasError(): boolean;
    clearError(): void;
    getError(): ErrorResponse | undefined;
    setError(value?: ErrorResponse): StreamResponse;

    hasBufferedInfo(): boolean;
    clearBufferedInfo(): void;
    getBufferedInfo(): BufferedEventInfo | undefined;
    setBufferedInfo(value?: BufferedEventInfo): StreamResponse;

    getPayloadCase(): StreamResponse.PayloadCase;

    serializeBinary(): Uint8Array;
    toObject(includeInstance?: boolean): StreamResponse.AsObject;
    static toObject(includeInstance: boolean, msg: StreamResponse): StreamResponse.AsObject;
    static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
    static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
    static serializeBinaryToWriter(message: StreamResponse, writer: jspb.BinaryWriter): void;
    static deserializeBinary(bytes: Uint8Array): StreamResponse;
    static deserializeBinaryFromReader(message: StreamResponse, reader: jspb.BinaryReader): StreamResponse;
}

export namespace StreamResponse {
    export type AsObject = {
        event?: RunningEvent.AsObject,
        error?: ErrorResponse.AsObject,
        bufferedInfo?: BufferedEventInfo.AsObject,
    }

    export enum PayloadCase {
        PAYLOAD_NOT_SET = 0,
        EVENT = 1,
        ERROR = 2,
        BUFFERED_INFO = 3,
    }

}

export class RegisterRequest extends jspb.Message { 
    getClientId(): string;
    setClientId(value: string): RegisterRequest;

    serializeBinary(): Uint8Array;
    toObject(includeInstance?: boolean): RegisterRequest.AsObject;
    static toObject(includeInstance: boolean, msg: RegisterRequest): RegisterRequest.AsObject;
    static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
    static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
    static serializeBinaryToWriter(message: RegisterRequest, writer: jspb.BinaryWriter): void;
    static deserializeBinary(bytes: Uint8Array): RegisterRequest;
    static deserializeBinaryFromReader(message: RegisterRequest, reader: jspb.BinaryReader): RegisterRequest;
}

export namespace RegisterRequest {
    export type AsObject = {
        clientId: string,
    }
}

export class RegisterResponse extends jspb.Message { 
    getSuccess(): boolean;
    setSuccess(value: boolean): RegisterResponse;
    getMessage(): string;
    setMessage(value: string): RegisterResponse;

    serializeBinary(): Uint8Array;
    toObject(includeInstance?: boolean): RegisterResponse.AsObject;
    static toObject(includeInstance: boolean, msg: RegisterResponse): RegisterResponse.AsObject;
    static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
    static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
    static serializeBinaryToWriter(message: RegisterResponse, writer: jspb.BinaryWriter): void;
    static deserializeBinary(bytes: Uint8Array): RegisterResponse;
    static deserializeBinaryFromReader(message: RegisterResponse, reader: jspb.BinaryReader): RegisterResponse;
}

export namespace RegisterResponse {
    export type AsObject = {
        success: boolean,
        message: string,
    }
}

export class UnregisterRequest extends jspb.Message { 
    getClientId(): string;
    setClientId(value: string): UnregisterRequest;

    serializeBinary(): Uint8Array;
    toObject(includeInstance?: boolean): UnregisterRequest.AsObject;
    static toObject(includeInstance: boolean, msg: UnregisterRequest): UnregisterRequest.AsObject;
    static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
    static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
    static serializeBinaryToWriter(message: UnregisterRequest, writer: jspb.BinaryWriter): void;
    static deserializeBinary(bytes: Uint8Array): UnregisterRequest;
    static deserializeBinaryFromReader(message: UnregisterRequest, reader: jspb.BinaryReader): UnregisterRequest;
}

export namespace UnregisterRequest {
    export type AsObject = {
        clientId: string,
    }
}

export class UnregisterResponse extends jspb.Message { 
    getSuccess(): boolean;
    setSuccess(value: boolean): UnregisterResponse;
    getMessage(): string;
    setMessage(value: string): UnregisterResponse;

    serializeBinary(): Uint8Array;
    toObject(includeInstance?: boolean): UnregisterResponse.AsObject;
    static toObject(includeInstance: boolean, msg: UnregisterResponse): UnregisterResponse.AsObject;
    static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
    static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
    static serializeBinaryToWriter(message: UnregisterResponse, writer: jspb.BinaryWriter): void;
    static deserializeBinary(bytes: Uint8Array): UnregisterResponse;
    static deserializeBinaryFromReader(message: UnregisterResponse, reader: jspb.BinaryReader): UnregisterResponse;
}

export namespace UnregisterResponse {
    export type AsObject = {
        success: boolean,
        message: string,
    }
}

export enum WeatherCondition {
    SUNNY = 0,
    CLOUDY = 1,
    RAINY = 2,
    STORMY = 3,
    SNOWY = 4,
}

export enum DistanceType {
    ULTRAMARATHON = 0,
    MARATHON = 1,
    HALF_MARATHON = 2,
    TEN_K = 3,
    FIVE_K = 4,
}
