import axios, { type AxiosRequestConfig } from "axios";

const instance = axios.create({
  timeout: 10_000,
});

export async function httpRequest<T = unknown>(
  url: string,
  options?: { method?: "GET" | "POST"; data?: unknown },
): Promise<T> {
  const config: AxiosRequestConfig = {
    url,
    method: options?.method ?? "GET",
    data: options?.data,
  };

  const response = await instance.request<T>(config);
  return response.data;
}
