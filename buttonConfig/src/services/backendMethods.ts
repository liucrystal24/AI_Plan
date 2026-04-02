import type { ButtonConfig } from "../types/button";
import { httpRequest } from "../utils/http";

const backendMethodMap: Record<
  string,
  (button: ButtonConfig) => Promise<unknown>
> = {
  ping: async () => {
    await new Promise((resolve) => setTimeout(resolve, 400));
    return { ok: true, message: "pong" };
  },
  submitButtonLog: async (button) => {
    return httpRequest("/api/button-log", {
      method: "POST",
      data: {
        buttonId: button.id,
        buttonText: button.text,
        timestamp: Date.now(),
      },
    });
  },
};

export async function callBackendMethod(
  methodName: string,
  button: ButtonConfig,
): Promise<unknown> {
  const method = backendMethodMap[methodName];
  if (!method) {
    throw new Error(`未找到后台方法: ${methodName}`);
  }
  return method(button);
}

export const availableBackendMethods = Object.keys(backendMethodMap);
