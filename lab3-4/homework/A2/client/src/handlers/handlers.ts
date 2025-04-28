import * as grpc from "@grpc/grpc-js";
import {
  RegisterRequest,
  UnregisterRequest,
  SubscriptionRequest,
  UnsubscribeRequest,
  StreamResponse,
  DistanceType,
  WeatherCondition,
} from "../../gen/run_pb";
import readline from "readline";
import { Subscription } from "../types/subscription";
import { createGrpcClient } from "./grpcClient";
import { printEnumOptions } from "../utils/enum-printer";
import { ActionResult } from "../types/action-result";
import { logEvent, logBuffered, logError, logWarn } from "../utils/logger";
import { resolve } from "path";

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

export const askQuestion = (query: string): Promise<string> =>
  new Promise((resolve) => rl.question(query, resolve));

export let clientId: string;
export let subscriptions: Subscription[] = [];
let listening = false;
let stream: grpc.ClientReadableStream<StreamResponse> | null = null;
export const client = createGrpcClient()!;

// REGISTER
export async function registerClient(): Promise<ActionResult> {
  clientId = await askQuestion("Enter your client ID (nickname): ");
  const req = new RegisterRequest();
  req.setClientId(clientId);

  return new Promise((resolve) => {
    client.register(req, (err, response) => {
      if (err) {
        resolve({
          success: false,
          message: "Registration failed: " + err.message,
          type: "error",
        });
      } else {
        resolve({
          success: true,
          message: response?.getMessage() || "Registered.",
          type: "info",
        });
      }
    });
  });
}

// UNREGISTER
export async function unregisterClient(): Promise<ActionResult> {
  const req = new UnregisterRequest();
  req.setClientId(clientId);

  return new Promise((resolve) => {
    client.unregister(req, (err, response) => {
      if (err) {
        resolve({
          success: false,
          message: "Unregister failed: " + err.message,
          type: "error",
        });
      } else if (response?.getSuccess()) {
        resolve({
          success: true,
          message: "Unregistered successfully.",
          type: "exit",
        });
      } else {
        resolve({
          success: false,
          message: "Unregister failed: " + response?.getMessage(),
          type: "error",
        });
      }
    });
  });
}

// SUBSCRIBE
export async function subscribe(): Promise<ActionResult> {
  const cities = (await askQuestion("Enter cities (comma-separated): "))
    .split(",")
    .map((s) => s.trim());

  printEnumOptions(DistanceType, "Distances");
  const distancesInput = (await askQuestion("Enter distances (e.g. 1,2,3): "))
    .split(",")
    .map((s) => parseInt(s.trim(), 10));

  printEnumOptions(WeatherCondition, "Weather conditions");
  const weatherInput = (
    await askQuestion("Enter weather conditions (e.g. 1,2): ")
  )
    .split(",")
    .map((s) => parseInt(s.trim(), 10));

  const tags = (await askQuestion("Enter tags (comma-separated): "))
    .split(",")
    .map((s) => s.trim());

  const req = new SubscriptionRequest();
  req.setClientId(clientId);
  req.setCitiesList(cities);
  req.setDistancesList(distancesInput);
  req.setTagsList(tags);
  req.setWeatherConditionsList(weatherInput);

  return new Promise((resolve) => {
    client.subscribe(req, (err, response) => {
      if (err) {
        resolve({
          success: false,
          message: "Subscription failed: " + err.message,
          type: "error",
        });
      } else if (!response.getSuccess()) {
        resolve({
          success: false,
          message: "Subscription error: " + response.getMessage(),
          type: "error",
        });
      } else {
        subscriptions.push({
          id: response.getSubscriptionId(),
          cities,
          distances: distancesInput,
          tags,
        });
        resolve({
          success: true,
          message: `Subscribed successfully. Subscription ID: ${response.getSubscriptionId()}`,
          type: "info",
        });
      }
    });
  });
}

// UNSUBSCRIBE
export async function unsubscribe(): Promise<ActionResult> {
  if (subscriptions.length === 0) {
    return {
      success: false,
      message: "No active subscriptions to unsubscribe from.",
      type: "info",
    };
  }

  console.log("Your subscriptions:");
  subscriptions.forEach((sub) =>
    console.log(
      `ID: ${sub.id} | Cities: ${sub.cities.join(
        ", "
      )} | Distances: ${sub.distances.join(", ")} | Tags: ${sub.tags.join(
        ", "
      )}`
    )
  );
  const subId = parseInt(
    await askQuestion("Enter subscription ID to unsubscribe: "),
    10
  );

  const req = new UnsubscribeRequest();
  req.setClientId(clientId);
  req.setSubscriptionId(subId);

  return new Promise((resolve) => {
    client.unsubscribe(req, (err, response) => {
      if (err) {
        resolve({
          success: false,
          message: "Unsubscribe failed: " + err.message,
          type: "error",
        });
      } else if (!response.getSuccess()) {
        resolve({
          success: false,
          message: "Unsubscribe error: " + response.getMessage(),
          type: "error",
        });
      } else {
        subscriptions = subscriptions.filter((sub) => sub.id !== subId);
        resolve({
          success: true,
          message: "Unsubscribed successfully.",
          type: "info",
        });
      }
    });
  });
}

// START LISTENING
export async function startListening(): Promise<ActionResult> {
  if (listening) {
    return { success: false, message: "Already listening.", type: "info" };
  }

  const req = new RegisterRequest();
  req.setClientId(clientId);
  stream = client.eventStream(req);
  listening = true;

  stream.on("data", (response: StreamResponse) => {
    if (response.hasEvent()) {
      const event = response.getEvent();
      logEvent(
        `ID: ${event?.getId()} | City: ${event?.getCity()} | Distance: ${event?.getDistance()} | Tags: ${event?.getTagsList()}`
      );
    } else if (response.hasBufferedInfo()) {
      logBuffered(
        `Buffered events: ${response.getBufferedInfo()?.getBufferedCount()}`
      );
    } else if (response.hasError()) {
      logError(response.getError()?.getErrorMessage() || "Unknown error.");
    }
  });

  stream.on("end", () => {
    logWarn("Stream ended.");
    listening = false;
  });

  stream.on("error", (err) => {
    logError("Stream error: " + err.message);
    listening = false;
  });

  return { success: true, message: "Listening started.", type: "info" };
}

// STOP LISTENING
export async function stopListening(): Promise<ActionResult> {
  if (stream) {
    stream.cancel();
    stream = null;
    listening = false;
    return { success: true, message: "Listening stopped.", type: "info" };
  } else {
    return {
      success: false,
      message: "Not currently listening.",
      type: "info",
    };
  }
}

// SHOW SUBSCRIPTIONS
export async function showSubscriptions(): Promise<ActionResult> {
  if (subscriptions.length === 0) {
    return {
      success: true,
      message: "No active subscriptions.",
      type: "info",
    };
  }

  const message = subscriptions
    .map(
      (sub) =>
        `ID: ${sub.id} | Cities: ${sub.cities.join(
          ", "
        )} | Distances: ${sub.distances.join(", ")} | Tags: ${sub.tags.join(
          ", "
        )}`
    )
    .join("\n");

  return {
    success: true,
    message: `Current subscriptions:\n${message}`,
    type: "info",
  };
}
