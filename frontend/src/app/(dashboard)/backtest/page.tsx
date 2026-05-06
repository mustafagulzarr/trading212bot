import { ScaffoldPage } from '@/components/scaffold-page';

export default function BacktestPage(): JSX.Element {
  return (
    <ScaffoldPage
      title="Backtest"
      description="Run historical simulations and compare equity curves against live performance."
    />
  );
}
