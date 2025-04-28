import {
  subscribe,
  unsubscribe,
  registerClient,
  askQuestion,
  startListening,
  stopListening,
  showSubscriptions,
  unregisterClient,
} from "./handlers/handlers";
import { ActionResult } from "./types/action-result";
import { logError, logInfo, logWarn } from "./utils/logger";

async function mainMenu() {
  await registerClient();

  let lastMessage: string | null = null;
  let lastMessageType: "info" | "error" | "warn" | "exit" | null = null;

  while (true) {
    console.log("\n=========================================");

    if (lastMessage) {
      switch (lastMessageType) {
        case "info":
          logInfo(lastMessage);
          break;
        case "error":
          logError(lastMessage);
          break;
        case "warn":
          logWarn(lastMessage);
          break;
        case "exit":
          logInfo(lastMessage);
          process.exit(0);
      }
      lastMessage = null;
      lastMessageType = null;
    }

    console.log("\n=== MENU ===");
    console.log("1. Subscribe");
    console.log("2. Unsubscribe");
    console.log("3. Start listening");
    console.log("4. Stop listening");
    console.log("5. Show subscriptions");
    console.log("6. Exit (Unregister)");

    const choice = await askQuestion("Choose an option: ");

    let result: ActionResult | null = null;

    switch (choice.trim()) {
      case "1":
        result = await subscribe();
        break;
      case "2":
        result = await unsubscribe();
        break;
      case "3":
        result = await startListening();
        break;
      case "4":
        result = await stopListening();
        break;
      case "5":
        result = await showSubscriptions();
        break;
      case "6":
        stopListening();
        result = await unregisterClient();
        break;
      default:
        result = {
          success: false,
          message: "Invalid option. Please try again.",
          type: "warn",
        };
    }

    if (result) {
      lastMessage = result.message;
      lastMessageType = result.type;
    }
  }
}

mainMenu();
