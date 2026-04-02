import { computed, ref, watch } from "vue";
import type { ButtonConfig } from "../types/button";

const STORAGE_KEY = "button-config-list";

const defaultButtons: ButtonConfig[] = [
  {
    id: crypto.randomUUID(),
    text: "打开官网",
    order: 1,
    style: {
      textColor: "#ffffff",
      backgroundColor: "#1f7a8c",
      borderColor: "#1f7a8c",
      borderRadius: 10,
      paddingY: 10,
      paddingX: 16,
      fontSize: 14,
    },
    action: {
      type: "link",
      payload: "https://www.vuejs.org",
    },
  },
  {
    id: crypto.randomUUID(),
    text: "调用后台Ping",
    order: 2,
    style: {
      textColor: "#0b3c49",
      backgroundColor: "#f1f5f9",
      borderColor: "#0b3c49",
      borderRadius: 10,
      paddingY: 10,
      paddingX: 16,
      fontSize: 14,
    },
    action: {
      type: "backend",
      payload: "ping",
    },
  },
];

function loadButtons(): ButtonConfig[] {
  const raw = localStorage.getItem(STORAGE_KEY);
  if (!raw) {
    return defaultButtons;
  }

  try {
    const parsed = JSON.parse(raw) as ButtonConfig[];
    if (!Array.isArray(parsed)) {
      return defaultButtons;
    }
    return parsed;
  } catch {
    return defaultButtons;
  }
}

const buttons = ref<ButtonConfig[]>(loadButtons());

watch(
  buttons,
  (value) => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(value));
  },
  { deep: true },
);

function createEmptyButton(order = buttons.value.length + 1): ButtonConfig {
  return {
    id: crypto.randomUUID(),
    text: "新按钮",
    order,
    style: {
      textColor: "#ffffff",
      backgroundColor: "#334155",
      borderColor: "#334155",
      borderRadius: 8,
      paddingY: 10,
      paddingX: 16,
      fontSize: 14,
    },
    action: {
      type: "link",
      payload: "",
    },
  };
}

function addButton(button?: ButtonConfig): ButtonConfig {
  const created = button ?? createEmptyButton();
  buttons.value.push(created);
  return created;
}

function updateButton(updatedButton: ButtonConfig): void {
  const index = buttons.value.findIndex((item) => item.id === updatedButton.id);
  if (index === -1) {
    return;
  }
  buttons.value[index] = updatedButton;
}

function removeButton(id: string): void {
  buttons.value = buttons.value.filter((item) => item.id !== id);
}

const sortedButtons = computed(() => {
  return [...buttons.value].sort((a, b) => a.order - b.order);
});

export function useButtonStore() {
  return {
    buttons,
    sortedButtons,
    createEmptyButton,
    addButton,
    updateButton,
    removeButton,
  };
}
