import { ScaffoldPage } from '@/components/scaffold-page';

export default function AuditPage(): JSX.Element {
  return (
    <ScaffoldPage
      title="Audit"
      description="Immutable log of trades, config changes, and system events."
    />
  );
}
