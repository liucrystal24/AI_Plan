import type { ActionType, ButtonConfig } from "../types/button";

interface ExportedButtonSchema {
  $schema: string;
  title: string;
  type: "object";
  description: string;
  properties: {
    buttons: {
      type: "array";
      description: string;
      items: {
        $ref: string;
      };
      default: ButtonConfig[];
    };
  };
  required: ["buttons"];
  additionalProperties: false;
  definitions: Record<string, unknown>;
}

const VALID_ACTION_TYPES: ActionType[] = ["link", "backend", "custom-js"];

export function buildButtonConfigSchema(
  buttons: ButtonConfig[],
): ExportedButtonSchema {
  return {
    $schema: "https://json-schema.org/draft/2020-12/schema",
    title: "ButtonConfigSchema",
    type: "object",
    description: "按钮配置 JSON Schema，包含配置结构和默认按钮快照。",
    properties: {
      buttons: {
        type: "array",
        description: "按钮配置列表，按 order 升序。",
        items: {
          $ref: "#/definitions/ButtonConfig",
        },
        default: buttons,
      },
    },
    required: ["buttons"],
    additionalProperties: false,
    definitions: {
      ButtonStyleConfig: {
        type: "object",
        properties: {
          textColor: { type: "string" },
          backgroundColor: { type: "string" },
          borderColor: { type: "string" },
          borderRadius: { type: "number" },
          paddingY: { type: "number" },
          paddingX: { type: "number" },
          fontSize: { type: "number" },
        },
        required: [
          "textColor",
          "backgroundColor",
          "borderColor",
          "borderRadius",
          "paddingY",
          "paddingX",
          "fontSize",
        ],
        additionalProperties: false,
      },
      ButtonActionConfig: {
        type: "object",
        properties: {
          type: {
            type: "string",
            enum: VALID_ACTION_TYPES,
          },
          payload: { type: "string" },
        },
        required: ["type", "payload"],
        additionalProperties: false,
      },
      ButtonConfig: {
        type: "object",
        properties: {
          id: { type: "string" },
          text: { type: "string" },
          order: { type: "number" },
          style: { $ref: "#/definitions/ButtonStyleConfig" },
          action: { $ref: "#/definitions/ButtonActionConfig" },
        },
        required: ["id", "text", "order", "style", "action"],
        additionalProperties: false,
      },
    },
  };
}

export function parseButtonsFromSchemaText(schemaText: string): ButtonConfig[] {
  const parsed = JSON.parse(schemaText) as unknown;

  if (Array.isArray(parsed)) {
    return validateButtonsArray(parsed);
  }

  if (!isObjectRecord(parsed)) {
    throw new Error("Schema 必须是对象或按钮数组");
  }

  if (Array.isArray(parsed.buttons)) {
    return validateButtonsArray(parsed.buttons);
  }

  const buttonsDefault = parsed.properties;
  if (!isObjectRecord(buttonsDefault)) {
    throw new Error("未找到 buttons 配置，请检查 Schema 格式");
  }

  const buttonsSchema = buttonsDefault.buttons;
  if (!isObjectRecord(buttonsSchema) || !Array.isArray(buttonsSchema.default)) {
    throw new Error("Schema 中未找到 properties.buttons.default");
  }

  return validateButtonsArray(buttonsSchema.default);
}

function validateButtonsArray(value: unknown[]): ButtonConfig[] {
  const result = value.map((item, index) => validateSingleButton(item, index));
  return result.sort((a, b) => a.order - b.order);
}

function validateSingleButton(value: unknown, index: number): ButtonConfig {
  if (!isObjectRecord(value)) {
    throw new Error(`第 ${index + 1} 个按钮配置不是对象`);
  }

  const style = value.style;
  const action = value.action;

  if (!isObjectRecord(style)) {
    throw new Error(`第 ${index + 1} 个按钮缺少 style`);
  }
  if (!isObjectRecord(action)) {
    throw new Error(`第 ${index + 1} 个按钮缺少 action`);
  }

  const actionType = String(action.type ?? "").trim() as ActionType;
  if (!VALID_ACTION_TYPES.includes(actionType)) {
    throw new Error(`第 ${index + 1} 个按钮 action.type 非法`);
  }

  return {
    id: String(value.id ?? ""),
    text: String(value.text ?? ""),
    order: Number(value.order ?? 0),
    style: {
      textColor: String(style.textColor ?? "#000000"),
      backgroundColor: String(style.backgroundColor ?? "#ffffff"),
      borderColor: String(style.borderColor ?? "#000000"),
      borderRadius: Number(style.borderRadius ?? 0),
      paddingY: Number(style.paddingY ?? 0),
      paddingX: Number(style.paddingX ?? 0),
      fontSize: Number(style.fontSize ?? 14),
    },
    action: {
      type: actionType,
      payload: String(action.payload ?? ""),
    },
  };
}

function isObjectRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null;
}
