import chalk from "chalk";

export const logInfo = (message: string) =>
  console.log(chalk.white("[INFO]"), message);
export const logWarn = (message: string) =>
  console.log(chalk.yellow("[WARN]"), message);
export const logError = (message: string) =>
  console.error(chalk.red("[ERROR]"), message);
export const logEvent = (message: string) =>
  console.log(chalk.green("[EVENT]"), message);
export const logBuffered = (message: string) =>
  console.log(chalk.blue("[BUFFERED]"), message);
