'use client';

import Link from 'next/link';

import { useDashboardData } from '@/hooks/useDashboardData';

export default function Home(): JSX.Element {
  const { summaryQuery, regimeQuery, ordersQuery } = useDashboardData();

  return (
    <main>
      <h1>Trading Bot Dashboard</h1>
      <p>Account summary: {summaryQuery.isSuccess ? 'loaded' : 'loading'}</p>
      <p>Current regime: {regimeQuery.isSuccess ? JSON.stringify(regimeQuery.data) : 'loading'}</p>
      <p>Orders loaded: {ordersQuery.isSuccess ? (ordersQuery.data as unknown[]).length : 0}</p>
      <nav>
        <Link href="/positions">Positions</Link> | <Link href="/orders">Orders</Link> | <Link href="/regime">Regime</Link> |{' '}
        <Link href="/strategies">Strategies</Link> | <Link href="/backtest">Backtest</Link> | <Link href="/compliance">Compliance</Link> |{' '}
        <Link href="/settings">Settings</Link> | <Link href="/audit">Audit</Link>
      </nav>
    </main>
  );
}
