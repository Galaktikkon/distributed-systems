export function printEnumOptions(enumObj: any, label: string): void {
  console.log(`\nChoose ${label}:`);
  Object.entries(enumObj)
    .filter(([key, value]) => typeof value === "number")
    .forEach(([key, value]) => {
      console.log(`${value}: ${key}`);
    });
}
