'use client';

import {
  Activity,
  BarChart3,
  ClipboardList,
  FileSearch,
  FlaskConical,
  LayoutDashboard,
  Layers,
  Settings,
  Shield,
  Wallet,
} from 'lucide-react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarRail,
  SidebarSeparator,
} from '@/components/ui/sidebar';

const mainNav = [
  { title: 'Dashboard', url: '/', icon: LayoutDashboard },
  { title: 'Positions', url: '/positions', icon: Wallet },
  { title: 'Orders', url: '/orders', icon: ClipboardList },
  { title: 'Regime', url: '/regime', icon: Activity },
  { title: 'Strategies', url: '/strategies', icon: Layers },
  { title: 'Backtest', url: '/backtest', icon: FlaskConical },
  { title: 'Compliance', url: '/compliance', icon: Shield },
  { title: 'Settings', url: '/settings', icon: Settings },
  { title: 'Audit', url: '/audit', icon: FileSearch },
] as const;

export function AppSidebar(): JSX.Element {
  const pathname = usePathname();

  return (
    <Sidebar collapsible="icon">
      <SidebarHeader className="border-b border-sidebar-border px-2 py-3">
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton
              size="lg"
              className="data-active:bg-sidebar-accent group-data-[collapsible=icon]:justify-center group-data-[collapsible=icon]:gap-0"
              isActive={pathname === '/'}
              render={<Link href="/" />}
            >
              <div className="flex aspect-square size-8 shrink-0 items-center justify-center rounded-lg bg-sidebar-primary text-sidebar-primary-foreground">
                <BarChart3 className="size-4 shrink-0" />
              </div>
              <div className="grid min-w-0 flex-1 text-left text-sm leading-tight group-data-[collapsible=icon]:hidden">
                <span className="truncate font-semibold">Trading212</span>
                <span className="truncate text-xs text-muted-foreground">Bot dashboard</span>
              </div>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarHeader>
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel>Overview</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {mainNav.map((item) => (
                <SidebarMenuItem key={item.url}>
                  <SidebarMenuButton
                    isActive={pathname === item.url}
                    tooltip={item.title}
                    render={<Link href={item.url} />}
                  >
                    <item.icon />
                    <span>{item.title}</span>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
      <SidebarSeparator />
      <SidebarFooter className="gap-2 p-2 text-xs text-muted-foreground">
        <p className="px-2 leading-relaxed group-data-[collapsible=icon]:hidden">
          Use the sidebar to navigate. Press{' '}
          <kbd className="rounded border bg-muted px-1 font-mono text-[0.7rem]">⌘B</kbd> to toggle.
        </p>
      </SidebarFooter>
      <SidebarRail />
    </Sidebar>
  );
}
