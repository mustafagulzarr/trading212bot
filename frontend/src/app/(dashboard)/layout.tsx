import type { ReactNode } from 'react';

import { DashboardShell } from '@/components/dashboard-shell';

export default function DashboardLayout({ children }: { children: ReactNode }): JSX.Element {
  return <DashboardShell>{children}</DashboardShell>;
}
