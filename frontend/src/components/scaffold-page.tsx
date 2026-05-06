import { ArrowLeft } from 'lucide-react';
import Link from 'next/link';

import { Button } from '@/components/ui/button';
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';

type ScaffoldPageProps = {
  title: string;
  description?: string;
};

export function ScaffoldPage({ title, description }: ScaffoldPageProps): JSX.Element {
  return (
    <div className="mx-auto w-full max-w-4xl space-y-8 p-4 md:p-6">
      <div>
        <h1 className="text-3xl font-semibold tracking-tight">{title}</h1>
        {description ? (
          <p className="text-muted-foreground mt-2 max-w-2xl text-sm">{description}</p>
        ) : null}
      </div>
      <Card>
        <CardHeader>
          <CardTitle>Coming soon</CardTitle>
          <CardDescription>
            This section is not implemented yet. Use the sidebar to explore other areas of the dashboard.
          </CardDescription>
        </CardHeader>
        <CardContent className="text-sm text-muted-foreground">
          {/* Phase 6 placeholder — replace with domain UI when backend endpoints land. */}
        </CardContent>
        <CardFooter>
          <Button variant="secondary" render={<Link href="/" />}>
            <ArrowLeft className="size-4" />
            Back to dashboard
          </Button>
        </CardFooter>
      </Card>
    </div>
  );
}
