import { ScaffoldPage } from '@/components/scaffold-page';

export default function OrdersPage(): JSX.Element {
  return (
    <ScaffoldPage
      title="Orders"
      description="Review and manage orders synced from Trading 212 via the trading API."
    />
  );
}
