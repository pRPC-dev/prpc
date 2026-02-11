import { baseOptions } from '@/lib/layout.shared';
import type { ReactNode } from 'react';

export default function Layout({ children }: { children: ReactNode }) {
  // HomeLayout is now handled in the root app/layout.tsx
  return <>{children}</>;
}
