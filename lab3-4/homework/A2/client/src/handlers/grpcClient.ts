import * as grpc from "@grpc/grpc-js";
import { RunningServiceClient } from "../../gen/run_grpc_pb";
import { logError } from "../utils/logger";

// 172.24.109.133

export function createGrpcClient(): RunningServiceClient | null {
  try {
    const client = new RunningServiceClient(
      "localhost:50051",
      grpc.credentials.createInsecure()
    );

    client.waitForReady(Date.now() + 3000, (err) => {
      if (err) {
        logError("Could not connect to the server. Is it running?");
        process.exit(1);
      }
    });

    return client;
  } catch (error) {
    logError("Failed to create gRPC client: " + error);
    return null;
  }
}
