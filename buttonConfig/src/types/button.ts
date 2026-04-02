export type ActionType = "link" | "backend" | "custom-js";

export interface ButtonStyleConfig {
  textColor: string;
  backgroundColor: string;
  borderColor: string;
  borderRadius: number;
  paddingY: number;
  paddingX: number;
  fontSize: number;
}

export interface ButtonActionConfig {
  type: ActionType;
  payload: string;
}

export interface ButtonConfig {
  id: string;
  text: string;
  order: number;
  style: ButtonStyleConfig;
  action: ButtonActionConfig;
}

export interface ActionExecutionContext {
  button: ButtonConfig;
  httpRequest: <T = unknown>(
    url: string,
    options?: { method?: "GET" | "POST"; data?: unknown },
  ) => Promise<T>;
  callBackendMethod: (
    methodName: string,
    button: ButtonConfig,
  ) => Promise<unknown>;
  showMessage: (message: string) => void;
}
