'use client';

import { useQuery } from '@tanstack/react-query';

import { API_BASES, apiGet } from '@/lib/api/client';

export function useDashboardData() {
  const summaryQuery = useQuery({
    queryKey: ['account-summary'],
    queryFn: () => apiGet(`${API_BASES.trading}/account/summary`),
  });

  const regimeQuery = useQuery({
    queryKey: ['current-regime'],
    queryFn: () => apiGet(`${API_BASES.strategy}/regime/current`),
  });

  const ordersQuery = useQuery({
    queryKey: ['orders'],
    queryFn: () => apiGet(`${API_BASES.trading}/orders`),
  });

  return { summaryQuery, regimeQuery, ordersQuery };
}
