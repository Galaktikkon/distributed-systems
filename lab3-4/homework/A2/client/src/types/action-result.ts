export type ActionResult = {
  success: boolean;
  message: string;
  type: "info" | "error" | "warn" | "exit";
};
