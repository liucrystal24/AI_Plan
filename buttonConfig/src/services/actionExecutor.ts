import type { ActionExecutionContext, ButtonConfig } from "../types/button";

export async function executeButtonAction(
  context: ActionExecutionContext,
): Promise<void> {
  const { button, showMessage } = context;
  const { type, payload } = button.action;

  if (type === "link") {
    if (!payload) {
      throw new Error("跳转链接不能为空");
    }
    window.open(payload, "_blank", "noopener,noreferrer");
    return;
  }

  if (type === "backend") {
    if (!payload) {
      throw new Error("后台方法名不能为空");
    }
    await context.callBackendMethod(payload, button);
    showMessage(`后台方法执行成功: ${payload}`);
    return;
  }

  if (!payload) {
    throw new Error("自定义 JS 不能为空");
  }

  console.log("执行自定义 JS:", payload);
  console.log(typeof payload);

  const runner = new Function("button", "utils", "showMessage", payload) as (
    button: ButtonConfig,
    utils: { httpRequest: ActionExecutionContext["httpRequest"] },
    showMessage: ActionExecutionContext["showMessage"],
  ) => unknown;

  await Promise.resolve(
    runner(button, { httpRequest: context.httpRequest }, showMessage),
  );
}
