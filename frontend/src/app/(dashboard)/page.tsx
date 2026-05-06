'use client';

import Link from 'next/link';

import { useDashboardData } from '@/hooks/useDashboardData';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Skeleton } from '@/components/ui/skeleton';
import { ArrowRight, CircleAlert, ClipboardList, Gauge, Wallet } from 'lucide-react';

function formatUpdatedAt(timestamp: number | undefined): string {
  if (timestamp === undefined) return '—';
  try {
    return new Date(timestamp).toLocaleString();
  } catch {
    return '—';
  }
}

function getOrderCount(data: unknown): string {
  if (Array.isArray(data)) return String(data.length);
  if (data && typeof data === 'object' && 'items' in data && Array.isArray((data as { items: unknown }).items)) {
    return String((data as { items: unknown[] }).items.length);
  }
  return '—';
}

function JsonPreview({ value, emptyLabel }: { value: unknown; emptyLabel: string }): JSX.Element {
  if (value === undefined || value === null) {
    return <p className="text-muted-foreground text-sm">{emptyLabel}</p>;
  }
  const text = JSON.stringify(value, null, 2);
  return (
    <ScrollArea className="h-[min(220px,40vh)] rounded-md border bg-muted/40 p-3">
      <pre className="whitespace-pre-wrap break-all font-mono text-xs leading-relaxed">{text}</pre>
    </ScrollArea>
  );
}

export default function Home(): JSX.Element {
  const { summaryQuery, regimeQuery, ordersQuery } = useDashboardData();

  return (
    <div className="mx-auto w-full max-w-6xl space-y-8 p-4 md:p-6">
      <div className="flex flex-col gap-2 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <h1 className="text-3xl font-semibold tracking-tight">Dashboard</h1>
          <p className="text-muted-foreground mt-2 max-w-2xl text-sm">
            Snapshot of your account, strategy regime, and orders. Connect the trading and strategy APIs to
            populate these cards.
          </p>
        </div>
        <Badge variant="secondary" className="w-fit shrink-0">
          Trading bot
        </Badge>
      </div>

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        <Card className="md:col-span-2 xl:col-span-1">
          <CardHeader className="flex flex-row items-start justify-between gap-2 space-y-0">
            <div>
              <CardTitle className="flex items-center gap-2 text-base">
                <Wallet className="size-4 opacity-80" aria-hidden />
                Account summary
              </CardTitle>
              <CardDescription>From trading API · GET /account/summary</CardDescription>
            </div>
            {summaryQuery.isFetching ? <Badge variant="outline">Updating…</Badge> : null}
          </CardHeader>
          <CardContent className="space-y-3">
            {summaryQuery.isLoading ? (
              <div className="space-y-2">
                <Skeleton className="h-4 w-3/4" />
                <Skeleton className="h-4 w-full" />
                <Skeleton className="h-4 w-5/6" />
              </div>
            ) : summaryQuery.isError ? (
              <Alert variant="destructive">
                <CircleAlert className="size-4" />
                <AlertTitle>Could not load summary</AlertTitle>
                <AlertDescription>
                  {summaryQuery.error instanceof Error ? summaryQuery.error.message : 'Request failed.'}
                </AlertDescription>
              </Alert>
            ) : (
              <JsonPreview value={summaryQuery.data} emptyLabel="No summary payload." />
            )}
          </CardContent>
          <CardFooter className="text-muted-foreground text-xs">
            Updated {formatUpdatedAt(summaryQuery.dataUpdatedAt)}
          </CardFooter>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-start justify-between gap-2 space-y-0">
            <div>
              <CardTitle className="flex items-center gap-2 text-base">
                <Gauge className="size-4 opacity-80" aria-hidden />
                Market regime
              </CardTitle>
              <CardDescription>Strategy API · GET /regime/current</CardDescription>
            </div>
            {regimeQuery.isSuccess ? (
              <Badge variant="secondary">Live</Badge>
            ) : regimeQuery.isLoading ? (
              <Badge variant="outline">…</Badge>
            ) : (
              <Badge variant="destructive">Error</Badge>
            )}
          </CardHeader>
          <CardContent className="space-y-3">
            {regimeQuery.isLoading ? (
              <div className="space-y-2">
                <Skeleton className="h-8 w-24" />
                <Skeleton className="h-4 w-full" />
              </div>
            ) : regimeQuery.isError ? (
              <Alert variant="destructive">
                <CircleAlert className="size-4" />
                <AlertTitle>Could not load regime</AlertTitle>
                <AlertDescription>
                  {regimeQuery.error instanceof Error ? regimeQuery.error.message : 'Request failed.'}
                </AlertDescription>
              </Alert>
            ) : (
              <JsonPreview value={regimeQuery.data} emptyLabel="No regime data." />
            )}
          </CardContent>
          <CardFooter className="text-muted-foreground text-xs">
            Updated {formatUpdatedAt(regimeQuery.dataUpdatedAt)}
          </CardFooter>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-base">
              <ClipboardList className="size-4 opacity-80" aria-hidden />
              Orders
            </CardTitle>
            <CardDescription>Trading API · GET /orders</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            {ordersQuery.isLoading ? (
              <>
                <Skeleton className="h-10 w-20" />
                <Skeleton className="h-4 w-full" />
              </>
            ) : ordersQuery.isError ? (
              <Alert variant="destructive">
                <CircleAlert className="size-4" />
                <AlertTitle>Could not load orders</AlertTitle>
                <AlertDescription>
                  {ordersQuery.error instanceof Error ? ordersQuery.error.message : 'Request failed.'}
                </AlertDescription>
              </Alert>
            ) : (
              <>
                <div className="flex items-baseline gap-2">
                  <span className="text-3xl font-semibold tabular-nums">{getOrderCount(ordersQuery.data)}</span>
                  <span className="text-muted-foreground text-sm">orders</span>
                </div>
                <p className="text-muted-foreground text-sm">
                  Last refreshed {formatUpdatedAt(ordersQuery.dataUpdatedAt)}
                </p>
              </>
            )}
          </CardContent>
          <CardFooter>
            <Button
              variant="outline"
              className="w-full sm:w-auto"
              render={<Link href="/orders" />}
            >
              View orders
              <ArrowRight className="size-4" />
            </Button>
          </CardFooter>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Quick navigation</CardTitle>
          <CardDescription>Open common workflow pages. Full navigation is always available in the sidebar.</CardDescription>
        </CardHeader>
        <CardContent className="flex flex-wrap gap-2">
          <Button variant="secondary" size="sm" render={<Link href="/positions" />}>
            Positions
          </Button>
          <Button variant="secondary" size="sm" render={<Link href="/regime" />}>
            Regime detail
          </Button>
          <Button variant="secondary" size="sm" render={<Link href="/strategies" />}>
            Strategies
          </Button>
          <Button variant="secondary" size="sm" render={<Link href="/backtest" />}>
            Backtest
          </Button>
          <Button variant="secondary" size="sm" render={<Link href="/compliance" />}>
            Compliance
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}
