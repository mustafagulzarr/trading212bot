import { ScaffoldPage } from '@/components/scaffold-page';

export default function SettingsPage(): JSX.Element {
  return (
    <ScaffoldPage
      title="Settings"
      description="API keys (server-side), feature flags, and environment preferences."
    />
  );
}
