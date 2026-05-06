const env = typeof process !== 'undefined' ? process.env : ({} as Record<string, string | undefined>);

export const API_BASES = {
  market: env.NEXT_PUBLIC_MARKET_API ?? 'http://localhost:8001',
  trading: env.NEXT_PUBLIC_TRADING_API ?? 'http://localhost:8002',
  strategy: env.NEXT_PUBLIC_STRATEGY_API ?? 'http://localhost:8003',
} as const;

export type ApiBase = keyof typeof API_BASES;

export class ApiError extends Error {
  constructor(
    message: string,
    readonly status: number,
    readonly url: string,
    readonly body: unknown,
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

async function request<T>(url: string, init?: RequestInit): Promise<T> {
  const response = await fetch(url, {
    ...init,
    headers: {
      'Accept': 'application/json',
      ...(init?.body ? { 'Content-Type': 'application/json' } : {}),
      ...(init?.headers ?? {}),
    },
  });

  const text = await response.text();
  const parsed: unknown = text ? safeJson(text) : null;

  if (!response.ok) {
    throw new ApiError(
      `${response.status} ${response.statusText} for ${url}`,
      response.status,
      url,
      parsed,
    );
  }

  return parsed as T;
}

function safeJson(text: string): unknown {
  try {
    return JSON.parse(text);
  } catch {
    return text;
  }
}

export function apiGet<T = unknown>(url: string, init?: RequestInit): Promise<T> {
  return request<T>(url, { ...init, method: 'GET' });
}

export function apiPost<T = unknown>(url: string, body?: unknown, init?: RequestInit): Promise<T> {
  return request<T>(url, {
    ...init,
    method: 'POST',
    body: body !== undefined ? JSON.stringify(body) : undefined,
  });
}

export function apiDelete<T = unknown>(url: string, init?: RequestInit): Promise<T> {
  return request<T>(url, { ...init, method: 'DELETE' });
}
